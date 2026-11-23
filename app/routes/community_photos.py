"""Local consent/settings and explicit per-photo community sharing."""
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit
from flask import Response, abort, Blueprint, current_app, flash, redirect, render_template, request, url_for
from sqlalchemy import text
from extensions import db
from utils import community_photo_client as service

community_photos_bp = Blueprint('community_photos', __name__, url_prefix='/community-photos')


def _record(aircraft_id):
    row = db.session.execute(text('SELECT AircraftID,Registration,Aircraft_Type,MSN,Aircraft_Image,ICAO_Address FROM aircraft WHERE AircraftID=:id'), {'id': aircraft_id}).mappings().first()
    if not row:
        return None, []
    names = [row['Aircraft_Image']] if row['Aircraft_Image'] else []
    names += list(db.session.execute(text('SELECT Filename FROM aircraft_images WHERE AircraftID=:id'), {'id': aircraft_id}).scalars())
    folder = Path(current_app.static_folder) / 'uploads/aircraft'
    names = [name for name in dict.fromkeys(names) if name and Path(name).name == name and (folder / name).is_file() and not (folder / name).is_symlink()]
    return dict(row), names


def _shareable_photo(name):
    """Pool provenance survives renames/sync in XMP; cached credit is hash-bound."""
    if not name or Path(name).name != name:
        return False
    path = Path(current_app.static_folder) / 'uploads/aircraft' / name
    if not path.is_file() or path.is_symlink():
        return False
    try:
        from utils.aircraft_photo_metadata import jpeg_xmp, parse_xmp, NS
        raw = path.read_bytes()
        if raw.startswith(b'\xff\xd8'):
            parsed = parse_xmp(jpeg_xmp(raw))
        else:
            from PIL import Image
            with Image.open(path) as image:
                parsed = parse_xmp(image.info.get('xmp', image.info.get('XML:com.adobe.xmp')))
        if parsed is not None and parsed.find('.//{'+NS+'}PhotoID') is not None:
            return False
        saved = service.credits().get(name, {})
        if saved.get('sha256'):
            import hashlib
            if hashlib.sha256(raw).hexdigest() == saved['sha256']:
                return False
        return True
    except (OSError, ValueError):
        return False


def _has_shareable_photo(aircraft):
    return any(_shareable_photo(photo.get('filename')) for photo in aircraft.get('carousel_images', []))


def maybe_share_upload(aircraft_id, filename):
    p = service.preferences()
    chosen = request.form.get('share_this_photo') == 'yes'
    own = request.form.get('own_photo') == 'yes'
    if not p['enabled'] or not (chosen or (p['auto_upload'] and own)):
        return
    if not own:
        flash('Photo saved in Logbook, but not shared: confirm that it is your own photo and suitable for public sharing.', 'warning')
        return
    row, names = _record(aircraft_id)
    if not row or filename not in names:
        return
    try:
        service.enqueue_owned_photo(Path(current_app.static_folder) / 'uploads/aircraft' / filename,
                                   row['Registration'], row['Aircraft_Type'], row['MSN'], explicit=True)
        flash('Your photo is queued privately for community submission. It will not be public until approved.', 'success')
        service.start_check(current_app._get_current_object())
    except Exception:
        flash('Your Logbook photo is saved. Community submission was not queued; check Community Photos settings before retrying.', 'warning')


@community_photos_bp.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        try:
            p = service.save_preferences(request.form)
            if p['enabled'] and not p.get('token'):
                service.request_access()
            flash('Community photo settings saved. Opting out stops future submissions; valid licences already granted cannot be recalled.', 'success')
        except (ValueError, OSError) as exc:
            flash(str(exc), 'warning')
        except Exception:
            flash('Settings saved locally. The repository is unavailable; no photos were sent.', 'warning')
        return redirect(url_for('community_photos.settings'))
    preferences = service.preferences()
    allowed = False
    if preferences['enabled']:
        try:
            allowed = service.download_headers(preferences) is not None
        except Exception:
            pass
    jobs = [service.read_json(path, {}) for path in (service.root() / 'outgoing').glob('*.json')]
    return render_template('community_photo_settings.html', preferences=preferences, download_allowed=allowed,
                           terms_version=service.TERMS_VERSION, license_url=service.LICENSE_URL,
                           library_url=url_for('community_photos.library'),
                           jobs=sorted(jobs, key=lambda job: job.get('consent_at', ''), reverse=True)[:20])


@community_photos_bp.post('/check')
def check():
    p = service.preferences()
    if p['enabled']:
        try:
            if not p.get('token'):
                service.request_access()
            else:
                status = service.access_status(p)
                with service.lock():
                    p = service.preferences();p['access_status'] = status
                    service.write_json(service.root() / 'preferences.json', p)
            flash('Contributor access checked. Pending requests need approval in AirTrack ATC.', 'info')
        except Exception:
            flash('The repository could not be reached. Local photos are unchanged.', 'warning')
    return redirect(url_for('community_photos.settings'))


@community_photos_bp.route('/share/<int:aircraft_id>', methods=['GET', 'POST'])
def share(aircraft_id):
    p = service.preferences()
    if not p['enabled'] or p['terms_version'] != service.TERMS_VERSION:
        return redirect(url_for('community_photos.settings'))
    aircraft, names = _record(aircraft_id)
    if not aircraft:
        return 'Aircraft not found', 404
    names = [name for name in names if _shareable_photo(name)]
    if not names:
        flash('There are no original photos available to share. Community pool photos cannot be submitted again.', 'info')
        return redirect(url_for('aircraft.aircraft_info', aircraft_id=aircraft_id))
    if request.method == 'POST':
        filename = request.form.get('filename', '')
        if filename not in names or request.form.get('own_photo') != 'yes':
            flash('Select a Logbook photo and confirm ownership, rights and privacy before sharing.', 'warning')
        else:
            try:
                service.enqueue_owned_photo(Path(current_app.static_folder) / 'uploads/aircraft' / filename,
                                            aircraft['Registration'], aircraft['Aircraft_Type'], aircraft['MSN'], explicit=True)
                flash('Queued privately. Contributor access and photo approval are required before public display.', 'success')
                service.start_check(current_app._get_current_object())
            except Exception:
                flash('The photo could not be queued. The local image is unchanged; check your contributor status.', 'warning')
        return redirect(url_for('community_photos.share', aircraft_id=aircraft_id))
    return render_template('community_photo_share.html', aircraft=aircraft, filenames=names,
                           license_url=service.LICENSE_URL, preferences=p)


def _download_headers():
    if not service.preferences()['enabled']:
        abort(404)
    try:
        headers = service.download_headers()
    except Exception:
        abort(503)
    if headers is None:
        abort(403)
    return headers


def _library_aircraft(aircraft_id):
    row = db.session.execute(text('SELECT AircraftID,Registration,Aircraft_Type,MSN,ICAO_Address FROM aircraft WHERE AircraftID=:id'), {'id': aircraft_id}).mappings().first()
    if not row:
        abort(404)
    return dict(row)


def _matching_photos(row, headers, page=1):
    if not row['MSN'] and not row['Aircraft_Type']:
        return []
    result = service.requests.get(service.BASE_URL + '/api/photo-library', params={
        'registration': row['Registration'], 'msn': row['MSN'] or '',
        'aircraft_type': row['Aircraft_Type'] or '', 'icao_hex': row.get('ICAO_Address') or '', 'page': page}, headers=headers, timeout=10, allow_redirects=False)
    if result.status_code in (401, 403):
        abort(403)
    result.raise_for_status()
    return [photo for photo in result.json()['photos']
            if photo.get('registration') == row['Registration']
            and (not row['MSN'] or str(photo.get('msn') or '').strip().casefold() == str(row['MSN']).strip().casefold())
            and (not row['Aircraft_Type'] or str(photo.get('aircraft_type') or '').strip().casefold() == str(row['Aircraft_Type']).strip().casefold())
            and (not row.get('ICAO_Address') or str(photo.get('icao_hex') or '').upper() == str(row['ICAO_Address']).upper())
            and isinstance(photo.get('access_grant'), str)]


@community_photos_bp.get('/library')
def library():
    headers = _download_headers()
    query = request.args.get('q', '').strip()[:100]
    try:
        page = max(1, min(int(request.args.get('page', '1')), 10000))
    except ValueError:
        page = 1
    choices = [dict(row) for row in db.session.execute(text("SELECT AircraftID,Registration,Aircraft_Type,MSN,ICAO_Address FROM aircraft WHERE (:q='' OR Registration LIKE :pattern OR Aircraft_Type LIKE :pattern) ORDER BY Registration LIMIT 100"), {'q':query, 'pattern':'%'+query+'%'}).mappings()]
    selected = None
    photos = []
    if request.args.get('aircraft_id'):
        try:
            selected = _library_aircraft(int(request.args['aircraft_id']))
            photos = _matching_photos(selected, headers, page)
        except ValueError:
            abort(404)
        except service.requests.RequestException:
            abort(503)
    response = Response(render_template('community_photo_library.html', photos=photos, query=query, page=page, aircraft_choices=choices, selected=selected), mimetype='text/html')
    response.headers['Cache-Control'] = 'private, no-store'
    return response


@community_photos_bp.get('/library/<photo_id>/image')
def library_image(photo_id):
    if not re.fullmatch('[0-9a-f]{32}', photo_id):
        abort(404)
    headers = _download_headers()
    try:
        aircraft_id = int(request.args.get('aircraft_id', ''))
    except ValueError:
        abort(404)
    row = _library_aircraft(aircraft_id)
    try:
        options = _matching_photos(row, headers, max(1, min(int(request.args.get('page', '1')), 10000)))
    except (ValueError, service.requests.RequestException):
        abort(503)
    photo = next((p for p in options if p['id'] == photo_id), None)
    if photo is None:
        abort(404)
    try:
        remote = service.requests.get(service.BASE_URL + '/photos/' + photo_id + '/image.jpg', headers={**headers, 'X-Photo-Grant': photo['access_grant']}, timeout=15, stream=True, allow_redirects=False)
    except service.requests.RequestException:
        abort(503)
    try:
        if remote.status_code in (401, 403, 404):
            abort(remote.status_code)
        remote.raise_for_status()
        content = bytearray()
        for chunk in remote.iter_content(65536):
            content.extend(chunk)
            if len(content) > service.MAX_BYTES:
                abort(502)
        if not content.startswith(b'\xff\xd8'):
            abort(502)
    finally:
        remote.close()
    response = Response(bytes(content), mimetype='image/jpeg')
    response.headers['Cache-Control'] = 'private, no-store'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    if request.args.get('download') == 'yes':
        response.headers['Content-Disposition'] = 'attachment; filename="COMM_' + photo_id + '.jpg"'
    return response


def init_community_photos(app):
    app.register_blueprint(community_photos_bp)
    @app.context_processor
    def community_context():
        p = service.preferences()
        def credit(url):
            name = unquote(urlsplit(str(url)).path.rsplit('/', 1)[-1])
            saved = service.credits().get(name)
            if saved:
                return saved
            if Path(name).name == name:
                try:
                    from utils.aircraft_photo_metadata import read_credit
                    return read_credit(Path(app.static_folder)/'uploads/aircraft'/name)
                except (OSError,ValueError):
                    pass
            return None
        return dict(community_sharing_enabled=p['enabled'] and p['terms_version'] == service.TERMS_VERSION,
                    community_auto_upload=p['auto_upload'], community_photo_credit=credit,
                    community_has_shareable_photo=_has_shareable_photo)
    @app.before_request
    def community_check():
        if request.method == 'GET' and not request.path.startswith('/static/'):
            service.start_check(app)
