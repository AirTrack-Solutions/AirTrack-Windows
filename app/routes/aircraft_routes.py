# AirTrack 1.0.0
# Copyright (c) 2025 Trevor (“Subhuti”). All rights reserved.
# SPDX-License-Identifier: LicenseRef-AirTrack-Proprietary-NC

import logging

import os

from datetime import date, datetime

from math import ceil

from typing import Any

from extensions import db

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from sqlalchemy import text

from werkzeug.utils import secure_filename

from utils.country_flags import get_country_flag

from utils.settings_utils import get_current_theme

# ---------------------------------------------------------------------------
# Time-zone helper (fallback if utils missing)
# ---------------------------------------------------------------------------
try:
    from utils.timezone_utils import convert_to_local  # type: ignore
except ImportError:  # Safe fallback

    def convert_to_local(dt):
        return dt


logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Blueprint Setup
# Canonical route: /aircraft/ (always ends with slash)
# ---------------------------------------------------------------------------
UPLOAD_SUBFOLDER: str = os.path.join('uploads', 'aircraft')
aircraft_bp = Blueprint('aircraft', __name__, url_prefix='/aircraft')


# ---------------------------------------------------------------------------
# Aircraft List – /aircraft/
# ---------------------------------------------------------------------------
@aircraft_bp.route('')

def aircraft_table():
    """Paginated, filterable aircraft table."""
    page = request.args.get("page", 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page

    airline_id = request.args.get("airlineID", type=int)
    reg_filter = request.args.get("registration", "").strip().upper()

    # ------------------ Filtering ------------------
    filters = []
    params: dict[str, Any] = {"limit": per_page, "offset": offset}

    if airline_id:
        filters.append("ac.AirlineID = :airlineID")
        params["airlineID"] = airline_id

    if reg_filter:
        filters.append("UPPER(ac.Registration) LIKE :registration")
        params["registration"] = f"%{reg_filter}%"

    where_clause = "WHERE " + " AND ".join(filters) if filters else ""

    # ------------------ Count Total -----------------
    total = (
        db.session.execute(
            text(f"SELECT COUNT(*) FROM aircraft ac {where_clause}"),
            params,
        ).scalar()
        or 0
    )
    total_pages = max(1, ceil(total / per_page))

    # ------------------ Fetch Page ------------------
    rows = db.session.execute(
        text(
            f"""
            SELECT ac.AircraftID, ac.Registration, ac.FlightNumber,
                ac.Aircraft_Type, ac.Departure, ac.Arrival,
                ac.Spotted_At, ac.Country_of_Reg, ac.First_Sighted,
                ac.Aircraft_Updated, ac.Aircraft_Image,
                al.AirlineName
            FROM aircraft ac
            LEFT JOIN airlines al ON ac.AirlineID = al.AirlineID
            {where_clause}
            ORDER BY ac.Aircraft_Updated DESC
            LIMIT :limit OFFSET :offset
            """
        ),
        params,
    ).fetchall()

    aircraft_list = []

    for row in rows:
        ac = dict(row._mapping)

        # Time formatting
        for fld in ("First_Sighted", "Aircraft_Updated"):
            dt = ac.get(fld)
            if isinstance(dt, date) and not isinstance(dt, datetime):
                dt = datetime.combine(dt, datetime.min.time())
            local = convert_to_local(dt) if dt else None
            ac[f"{fld}_Display"] = (
                local.strftime("%d-%m-%Y %H:%M:%S") if local else "Unknown"
            )

        # Country flag
        ac["Country_Flag"] = get_country_flag(ac.get("Country_of_Reg"))

        # Image if present
        if ac.get("Aircraft_Image"):
            ac["Image_URL"] = url_for(
                "static",
                filename=os.path.join(UPLOAD_SUBFOLDER, ac["Aircraft_Image"]),
            )

        aircraft_list.append(ac)

    # ------------------ Block Pagination Nav ------------------
    block_size = 10
    block_start = ((page - 1) // block_size) * block_size + 1
    block_end = min(block_start + block_size - 1, total_pages)
    prev_block = block_start - 1 if block_start > 1 else None
    next_block = block_end + 1 if block_end < total_pages else None

    return render_template(
        "aircraft_table.html",
        aircraft_list=aircraft_list,
        current_page=page,
        total_pages=total_pages,
        start_page=block_start,
        end_page=block_end,
        prev_block_page=prev_block,
        next_block_page=next_block,
        selected_airline_id=airline_id,
        selected_registration=reg_filter,
    )


# ---------------------------------------------------------------------------
# Aircraft Detail – /aircraft/aircraft_info/<id>
# ---------------------------------------------------------------------------
@aircraft_bp.route("/aircraft_info/<int:aircraft_id>", endpoint="aircraft_info")

def aircraft_info(aircraft_id):
    per_page = 10
    page = request.args.get("page", 1, type=int)

    row = db.session.execute(
        text(
            """
            SELECT ac.*, al.AirlineName, ac.Aircraft_Image,
                dap.AirportName AS DepartureName,
                dap.municipality AS DepartureCity,
                arp.AirportName AS ArrivalName,
                arp.municipality AS ArrivalCity
            FROM aircraft ac
            LEFT JOIN airlines al ON ac.AirlineID = al.AirlineID
            LEFT JOIN airports dap
                ON UPPER(TRIM(ac.Departure)) COLLATE utf8mb4_uca1400_ai_ci
                = UPPER(TRIM(dap.ICAO))     COLLATE utf8mb4_uca1400_ai_ci
            LEFT JOIN airports arp
                ON UPPER(TRIM(ac.Arrival))   COLLATE utf8mb4_uca1400_ai_ci
                = UPPER(TRIM(arp.ICAO))     COLLATE utf8mb4_uca1400_ai_ci
            WHERE ac.AircraftID = :id
            """
        ),
        {"id": aircraft_id},
    ).fetchone()

    if not row:
        flash("Aircraft not found.", "danger")
        return redirect(url_for("aircraft.aircraft_table"))

    aircraft = dict(row._mapping)

    # ------------------ Accurate Times Seen ------------------
    times_seen = db.session.execute(
        text("SELECT COUNT(*) FROM flights WHERE AircraftID = :id"),
        {"id": aircraft_id},
    ).scalar() or 0

    aircraft["Times_Seen"] = times_seen

    # ------------------ Last Sighted from flights table ------------------
    last_flight_ts = db.session.execute(
        text("SELECT MAX(Timestamp) FROM flights WHERE AircraftID = :id"),
        {"id": aircraft_id},
    ).scalar()

    if last_flight_ts:
        if isinstance(last_flight_ts, date) and not isinstance(last_flight_ts, datetime):
            last_flight_ts = datetime.combine(last_flight_ts, datetime.min.time())
        loc = convert_to_local(last_flight_ts)
        aircraft["Last_Sighted_Display"] = loc.strftime("%d-%m-%Y %H:%M:%S") if loc else "Unknown"
    else:
        aircraft["Last_Sighted_Display"] = "Unknown"

    aircraft["Country_Flag"] = get_country_flag(aircraft.get("Country_of_Reg"))

    # Age calculation
    try:
        yr = aircraft.get("Manufacture_Year")
        m_raw = aircraft.get("Manufacture_Month")

        if yr:
            if m_raw and str(m_raw).isdigit() and 1 <= int(m_raw) <= 12:
                month = int(m_raw)
            else:
                month = 1

            mfg = datetime(yr, month, 1)
            today = datetime.today()
            aircraft["Aircraft_Age"] = (
                today.year
                - mfg.year
                - ((today.month, today.day) < (mfg.month, mfg.day))
            )
        else:
            aircraft["Aircraft_Age"] = "Unknown"
    except Exception:
        logger.exception("Error computing manufacture data")
        aircraft["Aircraft_Age"] = "Unknown"

    # Time formatting
    for fld in ("First_Sighted", "Aircraft_Updated"):
        ts = aircraft.get(fld)
        if isinstance(ts, date) and not isinstance(ts, datetime):
            ts = datetime.combine(ts, datetime.min.time())
        loc = convert_to_local(ts) if ts else None
        aircraft[f"{fld}_Display"] = (
            loc.strftime("%d-%m-%Y %H:%M:%S") if loc else "Unknown"
        )

    # Image URL
    if aircraft.get("Aircraft_Image"):
        aircraft["Image_URL"] = url_for(
            "static",
            filename=os.path.join(UPLOAD_SUBFOLDER, aircraft["Aircraft_Image"]),
        )

    # ------------------ Flight History ------------------
    hist = db.session.execute(
        text(
            """
            SELECT
                FlightID,
                FlightNumber,
                Departure,
                Arrival,
                Timestamp,
                Spotted_At
            FROM flights
            WHERE Registration = :reg
            ORDER BY Timestamp DESC
            """
        ),
        {"reg": aircraft.get("Registration")},
    ).fetchall()

    history = []
    for rec in hist:
        d = dict(rec._mapping)
        ts = d.get("Timestamp")
        if isinstance(ts, date) and not isinstance(ts, datetime):
            ts = datetime.combine(ts, datetime.min.time())
        loc = convert_to_local(ts) if ts else None
        d["Timestamp_Display"] = (
            loc.strftime("%d-%m-%Y %H:%M:%S") if loc else "Unknown"
        )
        d["Spotted_At"] = d.get("Spotted_At") or "Unknown"
        history.append(d)

    # Simple pagination
    total_pages = max(1, ceil(len(history) / per_page))
    start_idx = (page - 1) * per_page
    paged = history[start_idx : start_idx + per_page]

    return render_template(
        "aircraft_info.html",
        aircraft=aircraft,
        flight_history=paged,
        current_page=page,
        total_pages=total_pages,
        current_year=datetime.now().year,
        selected_theme=get_current_theme(),
        cache_bust=int(datetime.utcnow().timestamp()),
    )


# ---------------------------------------------------------------------------
# Edit Aircraft – /aircraft/edit/<id>
# ---------------------------------------------------------------------------
@aircraft_bp.route("/edit/<int:aircraft_id>", methods=["GET", "POST"], endpoint="edit_aircraft")

def edit_aircraft(aircraft_id: int):
    """Edit an existing aircraft and optionally log a new flight."""

    # Fetch current aircraft record
    row = db.session.execute(
        text(
            """
            SELECT AircraftID, Registration, FlightNumber, Aircraft_Type, MSN,
                AirlineID, Spotted_At, Category, Country_of_Reg, Times_Seen,
                Sightings, Manufacture_Year, Manufacture_Month, ICAO_Address,
                Departure, Arrival, Notes
            FROM aircraft
            WHERE AircraftID = :id
            """
        ),
        {"id": aircraft_id},
    ).mappings().fetchone()

    if not row:
        flash("Aircraft not found.", "danger")
        return redirect(url_for("aircraft.aircraft_table"))

    aircraft = dict(row._mapping)

    # Fetch airlines for dropdown
    airline_rows = db.session.execute(
        text("SELECT AirlineID, AirlineName FROM airlines ORDER BY AirlineName")
    ).fetchall()
    airlines = [dict(r._mapping) for r in airline_rows]
    logger.info("✅ Airlines loaded for edit form: %s", airlines)

    if request.method == "POST":
        form = request.form
        save_mode = form.get("save_mode", "edit")

        registration = (form.get("Registration") or "").strip().upper()
        flight_number = (form.get("FlightNumber") or "").strip().upper()
        aircraft_type = form.get("Aircraft_Type") or ""
        msn = form.get("MSN") or ""
        spotted_at = form.get("Spotted_At") or ""
        category = form.get("Category") or ""
        country_of_reg = form.get("Country_of_Reg") or ""
        notes = form.get("Notes") or ""

        # Airline ID
        airline_id_raw = form.get("AirlineID") or ""
        airline_id = int(airline_id_raw) if airline_id_raw.isdigit() else None

        # Times seen
        times_seen_raw = (form.get("Times_Seen") or "").strip()
        times_seen = int(times_seen_raw) if times_seen_raw.isdigit() else 1

        # Manufacture year / month
        manufacture_year_raw = form.get("Manufacture_Year") or ""
        manufacture_year = (
            int(manufacture_year_raw) if manufacture_year_raw.isdigit() else None
        )

        manufacture_month_raw = form.get("Manufacture_Month") or "0"
        manufacture_month = (
            None
            if manufacture_month_raw in ("", "0")
            else int(manufacture_month_raw)
            if manufacture_month_raw.isdigit()
            else None
        )

        icao_address = (form.get("ICAO_Address") or "").strip()
        departure = (form.get("Departure") or "").strip().upper()
        arrival = (form.get("Arrival") or "").strip().upper()

        now_utc = datetime.utcnow()

        try:
            # ----------------- Update aircraft table -----------------
            db.session.execute(
                text(
                    """
                    UPDATE aircraft SET
                        AirlineID        = :AirlineID,
                        Registration     = :Registration,
                        FlightNumber     = :FlightNumber,
                        Aircraft_Type    = :Aircraft_Type,
                        MSN              = :MSN,
                        Category         = :Category,
                        Country_of_Reg   = :Country_of_Reg,
                        Times_Seen       = :Times_Seen,
                        Manufacture_Year = :Manufacture_Year,
                        Manufacture_Month= :Manufacture_Month,
                        ICAO_Address     = :ICAO_Address,
                        Spotted_At       = :Spotted_At,
                        Notes            = :Notes,
                        Departure        = :Departure,
                        Arrival          = :Arrival,
                        Aircraft_Updated = :Aircraft_Updated
                    WHERE AircraftID     = :AircraftID
                    """
                ),
                {
                    "AirlineID": airline_id,
                    "Registration": registration,
                    "FlightNumber": flight_number,
                    "Aircraft_Type": aircraft_type,
                    "MSN": msn,
                    "Category": category,
                    "Country_of_Reg": country_of_reg,
                    "Times_Seen": times_seen,
                    "Manufacture_Year": manufacture_year,
                    "Manufacture_Month": manufacture_month,
                    "ICAO_Address": icao_address,
                    "Spotted_At": spotted_at,
                    "Notes": notes,
                    "Departure": departure,
                    "Arrival": arrival,
                    "Aircraft_Updated": now_utc,
                    "AircraftID": aircraft_id,
                },
            )

            # ----------------- Optional: log a new flight -------------
            if save_mode == "new":
                db.session.execute(
                    text(
                        """
                        INSERT INTO flights (
                            AircraftID,
                            AirlineID,
                            FlightNumber,
                            Registration,
                            MSN,
                            Aircraft_Type,
                            Times_Seen,
                            Departure,
                            Arrival,
                            Country_of_Reg,
                            Timestamp,
                            Spotted_At
                        ) VALUES (
                            :AircraftID,
                            :AirlineID,
                            :FlightNumber,
                            :Registration,
                            :MSN,
                            :Aircraft_Type,
                            :Times_Seen,
                            :Departure,
                            :Arrival,
                            :Country_of_Reg,
                            :Timestamp,
                            :Spotted_At
                        )
                        """
                    ),
                    {
                        "AircraftID": aircraft_id,
                        "AirlineID": airline_id,
                        "FlightNumber": flight_number,
                        "Registration": registration,
                        "MSN": msn,
                        "Aircraft_Type": aircraft_type,
                        "Times_Seen": times_seen,
                        "Departure": departure,
                        "Arrival": arrival,
                        "Country_of_Reg": country_of_reg,
                        "Timestamp": now_utc,
                        "Spotted_At": spotted_at,
                    },
                )

            db.session.commit()

            if save_mode == "new":
                flash("Aircraft updated and new flight logged.", "success")
            else:
                flash("Aircraft updated successfully.", "success")

            return redirect(url_for("aircraft.aircraft_info", aircraft_id=aircraft_id))

        except Exception as e:
            db.session.rollback()
            logger.exception("❌ Failed to update aircraft")
            flash(f"Failed to update aircraft: {e}", "danger")
            # fall through to re-render form with old values

    # GET path → render form

    return render_template(
        "edit_aircraft.html",
        aircraft=aircraft,
        airlines=airlines,
        selected_theme=get_current_theme(),
        cache_bust=int(datetime.utcnow().timestamp()),
    )


# ---------------------------------------------------------------------------
# Upload aircraft image – /aircraft/upload
# ---------------------------------------------------------------------------
@aircraft_bp.route("/upload", methods=["GET", "POST"])

def upload_aircraft_image():
    if request.method == "POST":
        airline_id = request.form.get("airline")
        registration = request.form.get("registration")
        image = request.files.get("image")

        if not all([airline_id, registration, image]):
            flash("Airline, registration, and image are all required.", "danger")
            return redirect(url_for("aircraft.upload_aircraft_image"))

        ts = datetime.now().strftime("%Y%m%d%H%M%S")
        original = secure_filename(getattr(image, "filename", "") or "")
        filename = (
            secure_filename(f"{registration}_{ts}_{original}")
            if original
            else secure_filename(f"{registration}_{ts}")
        )

        upload_dir = os.path.join(str(current_app.static_folder), UPLOAD_SUBFOLDER)
        os.makedirs(upload_dir, exist_ok=True)
        filepath = os.path.join(upload_dir, filename)

        try:
            image.save(filepath)
            with db.engine.begin() as conn:
                conn.execute(
                    text(
                        "UPDATE aircraft SET Aircraft_Image = :fn, "
                        "Aircraft_Updated = NOW() WHERE Registration = :reg"
                    ),
                    {"fn": filename, "reg": registration},
                )
            flash("Image uploaded successfully!", "success")
        except Exception:
            logger.exception("❌ Failed image upload")
            flash("Failed to upload image or update database.", "danger")

        return redirect(url_for("aircraft.aircraft_table"))

    # GET request → load airlines
    try:
        airlines = [
            dict(r._mapping)
            for r in db.session.execute(
                text("SELECT AirlineID, AirlineName FROM airlines ORDER BY AirlineName")
            ).fetchall()
        ]
    except Exception:
        logger.exception("❌ Airline list load error")
        airlines = []

    return render_template(
        "upload_aircraft_image.html",
        airlines=airlines,
        selected_theme=get_current_theme(),
        cache_bust=int(datetime.utcnow().timestamp()),
    )


# ---------------------------------------------------------------------------
# Delete aircraft image – /aircraft/delete_image/<id>
# ---------------------------------------------------------------------------
@aircraft_bp.route("/delete_image/<int:aircraft_id>", methods=["POST"])

def delete_image(aircraft_id):
    """Remove aircraft image file and clear DB reference."""
    try:
        with db.engine.begin() as conn:
            fn_row = conn.execute(
                text("SELECT Aircraft_Image FROM aircraft WHERE AircraftID = :id"),
                {"id": aircraft_id},
            ).fetchone()

            if fn_row and fn_row[0]:
                filename = str(fn_row[0])
                path = os.path.join(
                    str(current_app.static_folder), UPLOAD_SUBFOLDER, filename
                )

                if os.path.exists(path):
                    os.remove(path)

                conn.execute(
                    text(
                        "UPDATE aircraft "
                        "SET Aircraft_Image = NULL "
                        "WHERE AircraftID = :id"
                    ),
                    {"id": aircraft_id},
                )

        flash("Image deleted successfully.", "success")
        return redirect(url_for("aircraft.aircraft_info", aircraft_id=aircraft_id))

    except Exception:
        logger.exception("❌ Failed to delete image")
        flash("Could not delete image.", "danger")
        return redirect(url_for("aircraft.aircraft_info", aircraft_id=aircraft_id))