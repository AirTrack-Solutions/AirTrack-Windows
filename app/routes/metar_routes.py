# AirTrack Solutions — ATC METARs Route
# Copyright (c) 2025 AirTrack Solutions (ABN 70 472 536 433). All rights reserved.
# SPDX-License-Identifier: LicenseRef-AirTrack-Proprietary

"""Logbook METAR display, adapted from ATC's tested weather decoder.
Reads the existing metar_stations setting, uses cached AWC/NOAA/BOM fallbacks,
and displays existing history. No settings writes, schema creation or background
poller: existing collectors remain responsible for history.
"""

from __future__ import annotations

import json
import math
import os
import random
import re
import threading
import time
from datetime import datetime, timedelta, timezone
from urllib.error import URLError
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

import pymysql
import pymysql.cursors
try:
    from astral import Observer
    from astral.sun import sun
except ImportError:
    Observer = sun = None

from flask import Blueprint, abort, render_template, request
from extensions import db
from utils.settings_utils import get_current_theme

metars_bp = Blueprint("metars", __name__, url_prefix="/metars")

_AWC_METAR_URL = "https://aviationweather.gov/api/data/metar?ids={icao}&format=json"
_AWC_TIMEOUT = int(os.environ.get("AWC_METAR_TIMEOUT", "10"))

_TEXT_METAR_URL = "https://tgftp.nws.noaa.gov/data/observations/metar/stations/{icao}.TXT"
_TEXT_METAR_TIMEOUT = int(os.environ.get("TEXT_METAR_TIMEOUT", "10"))

_BOM_URL = "https://www.bom.gov.au/fwo/{product_id}/{product_id}.{station_id}.json"
_BOM_TIMEOUT = int(os.environ.get("BOM_TIMEOUT", "10"))

# Manual ICAO -> (product_id, station_id) map for the BOM last-resort
# fallback. Confirmed working pairs only — see docstring above.
_BOM_STATIONS = {
    "YSWS": ("IDN60901", "94149"),  # Western Sydney International (Nancy-Bird Walton)
    "YSBK": ("IDN60901", "94765"),  # Bankstown Airport AWS
    "YSCN": ("IDN60901", "94755"),  # Camden Airport AWS
    "YSHL": ("IDN60801", "95748"),  # Shellharbour Airport / Albion Park AWS
}

# Nicer display names for stations the text-mirror/BOM paths don't hand us
# a full name for.
_STATION_NAMES = {
    "YSWS": "Western Sydney International (Nancy-Bird Walton) Airport",
    "YSBK": "Bankstown Airport",
    "YSCN": "Camden Airport",
}

_KT_TO_KMH = 1.852
_MPS_TO_KT = 1.94384
_M_TO_SM = 1 / 1609.34

_COMPASS = [
    "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
    "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW",
]

_FC_COLORS = {
    "VFR": "#63ff95",
    "MVFR": "#7fb7ff",
    "IFR": "#ff5f5f",
    "LIFR": "#ff5fe8",
}

_CLOUD_RE = re.compile(r"^(FEW|SCT|BKN|OVC|VV)(\d{3})(CB|TCU)?$")
_WIND_RE = re.compile(r"^(\d{3}|VRB)(\d{2,3})(?:G(\d{2,3}))?(KT|MPS)$")
_TEMP_RE = re.compile(r"^(M?\d{2})/(M?\d{2})?$")

# Simple in-process cache so switching color or re-visiting the page doesn't
# hammer AWC/NOAA/BOM on every request. Keyed by ICAO, value is
# (fetched_at, decoded dict | None).
_CACHE_TTL = int(os.environ.get("AWC_METAR_CACHE_TTL", "300"))
_cache: dict[str, tuple[float, dict | None]] = {}

# ---------------------------------------------------------------------------
# Dashboard extras: runways (crosswind), coordinates (daylight), glossary,
# plain-language summaries, and trend history — all keyed by ICAO like the
# BOM/name maps above, since there's no lookup API for any of this either.
# ---------------------------------------------------------------------------

# (lat, lon) — used for sunrise/sunset only, doesn't need survey precision.
_COORDS = {
    "YSSY": (-33.9461, 151.1772),
    "YSBK": (-33.9243, 150.9885),
    "YSCN": (-34.0397, 150.6881),
    "YSRI": (-33.6003, 150.7811),
    "YSWS": (-33.8917, 150.7247),
}

_TIMEZONES = {
    "YSSY": "Australia/Sydney",
    "YSBK": "Australia/Sydney",
    "YSCN": "Australia/Sydney",
    "YSRI": "Australia/Sydney",
    "YSWS": "Australia/Sydney",
}

# Runway idents, in physical pairs. Headings are derived from the idents
# themselves (e.g. "16R" -> 160 deg) rather than surveyed true headings —
# accurate to within a few degrees of magnetic variation, which is fine for
# an at-a-glance crosswind indicator but NOT for actual flight planning.
_RUNWAYS = {
    "YSSY": [("07", "25"), ("16L", "34R"), ("16R", "34L")],
    "YSBK": [("11L", "29R"), ("11C", "29C"), ("11R", "29L")],
    "YSCN": [("06", "24"), ("10", "28")],
    "YSRI": [("10", "28")],
    "YSWS": [("05", "23")],
    "YSHL": [("08", "26")],
}

_FC_MEANINGS = {
    "VFR": "Visual Flight Rules — good weather, pilots can navigate by looking outside.",
    "MVFR": "Marginal VFR — workable, but pilots need to stay alert and may lean on instruments.",
    "IFR": "Instrument Flight Rules — poor visibility or low cloud; pilots must fly using instruments.",
    "LIFR": "Low IFR — very poor visibility or very low cloud; only well-equipped aircraft can operate.",
}

_GLOSSARY = {
    "flight_cat": "A simple traffic-light summary of how good conditions are for flying, based on cloud ceiling and visibility.",
    "temp": "The current air temperature at the airport.",
    "wind": "The direction the wind is blowing FROM, and its steady speed.",
    "gust": "A brief spike in wind speed above the steady wind reading.",
    "visibility": "How far you can see horizontally in the current conditions.",
    "ceiling": "The height of the lowest cloud layer that covers more than half the sky. A low ceiling means low-flying cloud.",
    "qnh": "The local air pressure setting, used to set an aircraft's altimeter so it reads correct height above sea level.",
    "dewpoint": "The temperature air needs to cool to for fog or dew to form — the closer to the actual temperature, the more likely fog is.",
    "cloud": "The amount and height of cloud layers reported (e.g. BKN = broken, OVC = overcast).",
    "weather": "Any precipitation or obscuration being reported, like rain, drizzle or fog.",
    "crosswind": "The part of the wind blowing across a runway rather than along it. Higher crosswind makes landing and takeoff trickier.",
    "headwind": "The part of the wind blowing straight down a runway, which helps aircraft take off and land in a shorter distance.",
    "daylight": "Sunrise and sunset times, and how far through today's daylight hours it currently is.",
    "trend": "How temperature and wind speed have changed at this station recently.",
}

_WX_PLAIN = {
    "RA": "rain", "-RA": "light rain", "+RA": "heavy rain",
    "SHRA": "rain showers", "-SHRA": "light rain showers", "+SHRA": "heavy rain showers",
    "DZ": "drizzle", "TS": "thunderstorms", "TSRA": "thunderstorms with rain",
    "VCTS": "thunderstorms in the vicinity", "BR": "mist", "FG": "fog",
    "HZ": "haze", "SN": "snow", "GR": "hail", "GS": "small hail", "SQ": "squalls",
    "FC": "funnel cloud", "FU": "smoke", "DU": "dust", "SA": "sand",
}

# Trend history: how far apart successive rows must be before we bother
# inserting another one, and how often the background poller wakes up.
_HISTORY_MIN_GAP_MINUTES = 10
_POLLER_INTERVAL_SECONDS = int(os.environ.get("METAR_POLLER_INTERVAL", str(15 * 60)))
_poller_started = False
_poller_lock = threading.Lock()


# ---------------------------------------------------------------------------
# DB helper
# ---------------------------------------------------------------------------

def _db() -> pymysql.Connection:
    # Use Logbook's actual configured engine, including its port.
    url = db.engine.url
    return pymysql.connect(
        host=url.host or "127.0.0.1", port=url.port or 3306,
        user=url.username, password=url.password, database=url.database,
        charset="utf8mb4", autocommit=False,
        cursorclass=pymysql.cursors.DictCursor,
    )


def _load_stations() -> list[str]:
    """Use the existing Logbook settings; an explicitly empty list stays empty."""
    raw = os.environ.get("METAR_STATIONS", "")
    try:
        conn = _db()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT SettingValue FROM app_settings WHERE SettingKey = 'metar_stations'")
                row = cur.fetchone()
                if row is not None:
                    raw = row.get("SettingValue") or ""
        finally:
            conn.close()
    except Exception:
        pass
    return sorted({s.strip().upper() for s in raw.split(",") if re.fullmatch(r"[A-Z]{4}", s.strip().upper())})


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _compass(deg) -> str:
    if deg is None:
        return ""
    try:
        return _COMPASS[round(float(deg) / 22.5) % 16]
    except (TypeError, ValueError):
        return ""


def _compass_to_deg(compass: str | None) -> float | None:
    """Reverse of _compass() — BOM's fwo feed only gives a 16-point compass
    string (e.g. "W"), not a numeric heading, so approximate the degree at
    the midpoint of that 22.5-degree sector. Needed for the wind compass
    arrow and runway crosswind table, both of which no-op on wind_dir_deg
    being None."""
    if not compass:
        return None
    try:
        return float(_COMPASS.index(compass.strip().upper()) * 22.5)
    except ValueError:
        return None


def _to_float(value) -> float | None:
    """Best-effort float parse — handles AWC's occasional '6+' visibility
    strings and BOM's occasional '-' placeholder or '>10' style values."""
    if value in (None, "", "-"):
        return None
    try:
        return float(str(value).rstrip("+").lstrip(">"))
    except ValueError:
        return None


def _classify_flight_category(ceiling_ft: float | None, vis_sm: float | None) -> tuple[str, str]:
    """Standard FAA ceiling/visibility flight-category rule."""
    if ceiling_ft is None and vis_sm is None:
        return "", ""
    ceiling_val = ceiling_ft if ceiling_ft is not None else 99999
    vis_val = vis_sm if vis_sm is not None else 99
    if ceiling_val < 500 or vis_val < 1:
        cat = "LIFR"
    elif ceiling_val < 1000 or vis_val < 3:
        cat = "IFR"
    elif ceiling_val <= 3000 or vis_val <= 5:
        cat = "MVFR"
    else:
        cat = "VFR"
    return cat, _FC_COLORS.get(cat, "#7da892")


_MAX_OBSERVATION_AGE = int(os.getenv("METAR_MAX_AGE_SECONDS", "7200"))


def _utc_time(value):
    try:
        if isinstance(value, (int, float)):
            return datetime.fromtimestamp(value, timezone.utc)
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return parsed.replace(tzinfo=timezone.utc) if parsed.tzinfo is None else parsed.astimezone(timezone.utc)
    except (ValueError, TypeError, OverflowError, OSError):
        return None


def _text_time(raw, reference=None):
    reference = reference or datetime.now(timezone.utc)
    match = re.search(r"\b(\d{2})(\d{2})(\d{2})Z\b", raw)
    if not match:
        return None
    day, hour, minute = map(int, match.groups())
    candidates = []
    for offset in (-1, 0, 1):
        month_index = reference.year * 12 + reference.month - 1 + offset
        year, month = divmod(month_index, 12)
        try:
            candidates.append(datetime(year, month + 1, day, hour, minute, tzinfo=timezone.utc))
        except ValueError:
            pass
    return min(candidates, key=lambda dt: abs((dt-reference).total_seconds())) if candidates else None


def _freshness(d, now=None):
    if not d:
        return d
    now = now or datetime.now(timezone.utc)
    observed = _utc_time(d.get("observed_at_utc"))
    age = (now-observed).total_seconds() if observed else None
    d["is_current"] = age is not None and -600 <= age <= _MAX_OBSERVATION_AGE
    d["freshness_warning"] = ""
    if observed:
        local = observed.astimezone(ZoneInfo(_TIMEZONES.get(d["icao"], "Australia/Sydney")))
        d["obs_time"] = local.strftime("%d %b %Y %H:%M %Z") + " / " + observed.strftime("%H:%M UTC")
        d["age_display"] = f"{max(0, int(age // 3600))}h {max(0, int(age // 60)) % 60}m old" if age >= 0 else "future timestamp"
    else:
        d["obs_time"] = "time unavailable"
        d["age_display"] = "age unknown"
    if not d["is_current"]:
        d["freshness_warning"] = ("STALE OBSERVATION — historical data, not current weather." if age is not None and age > _MAX_OBSERVATION_AGE else "OBSERVATION TIME UNVERIFIED — do not treat this as current weather.")
        d["summary"] = d["freshness_warning"]
        d["flight_cat"] = ""
        d["flight_cat_color"] = ""
    return d


def _base_fields(icao: str) -> dict:
    """Default/empty values for every field the template expects, so each
    decoder only has to override what it actually knows."""
    return {
        "icao": icao,
        "name": _STATION_NAMES.get(icao, icao),
        "raw": "",
        "obs_time": "",
        "source": "",
        "flight_cat": "",
        "flight_cat_color": "",
        "temp_c": None,
        "dewpoint_c": None,
        "wind_kmh": 0,
        "gust_kmh": 0,
        "wind_dir_compass": "",
        "wind_dir_deg": None,
        "visib_km": None,
        "visib_unlimited": False,
        "altim_hpa": None,
        "wx_string": "",
        "clouds": "",
        "ceiling_display": "—",
    }


# ---------------------------------------------------------------------------
# Source 1: AWC METAR JSON
# ---------------------------------------------------------------------------

def _fetch_awc_raw(icao: str) -> dict | None:
    url = _AWC_METAR_URL.format(icao=icao)
    req = Request(url, headers={"User-Agent": "AirTrack-ATC/1.0 (metars page)"})
    try:
        with urlopen(req, timeout=_AWC_TIMEOUT) as resp:
            records = json.loads(resp.read().decode("utf-8", errors="replace"))
        if isinstance(records, list) and records:
            return records[0]
    except (URLError, json.JSONDecodeError, TimeoutError, OSError):
        pass
    return None


def _decode_awc(record: dict, icao: str) -> dict:
    d = _base_fields(icao)
    wind_kt = record.get("wspd") or 0
    gust_kt = record.get("wgst") or 0
    visib_raw = record.get("visib")
    wdir = record.get("wdir")

    clouds = record.get("clouds") or []
    ceiling_ft = None
    for c in clouds:
        cov, base = c.get("cover"), c.get("base")
        if cov in ("BKN", "OVC", "VV") and isinstance(base, (int, float)):
            if ceiling_ft is None or base < ceiling_ft:
                ceiling_ft = base
    cloud_str = ", ".join(
        f"{c.get('cover', '')} {round(c.get('base') * 0.3048)} m".strip()
        for c in clouds
        if c.get("cover") not in (None, "SKC", "CLR") and isinstance(c.get("base"), (int, float))
    ) or ("Sky clear" if clouds or record.get("cover") in ("SKC", "CLR") else "")

    flight_cat = (record.get("fltCat") or "").upper()

    visib_val = _to_float(visib_raw)
    visib_unlimited = isinstance(visib_raw, str) and visib_raw.rstrip().endswith("+")
    visib_km = 10.0 if visib_unlimited else (round(visib_val * 1.60934, 1) if visib_val is not None else None)

    d.update({
        "name": record.get("name") or d["name"],
        "raw": record.get("rawOb", ""),
        "obs_time": record.get("reportTime", ""),
        "observed_at_utc": record.get("obsTime") or record.get("reportTime"),
        "source": "AWC",
        "flight_cat": flight_cat,
        "flight_cat_color": _FC_COLORS.get(flight_cat, "#7da892"),
        "temp_c": record.get("temp"),
        "dewpoint_c": record.get("dewp"),
        "wind_kmh": round(wind_kt * _KT_TO_KMH, 1) if wind_kt else 0,
        "gust_kmh": round(gust_kt * _KT_TO_KMH, 1) if gust_kt else 0,
        "wind_dir_compass": _compass(wdir),
        "wind_dir_deg": wdir if isinstance(wdir, (int, float)) else None,
        "visib_km": visib_km,
        "visib_unlimited": visib_unlimited,
        "altim_hpa": record.get("altim"),
        "wx_string": record.get("wxString", ""),
        "clouds": cloud_str,
        "ceiling_display": f"{round(ceiling_ft * 0.3048):,} m" if ceiling_ft is not None else "None",
    })
    return d


# ---------------------------------------------------------------------------
# Source 2: NOAA raw METAR text mirror (parsed ourselves)
# ---------------------------------------------------------------------------

def _fetch_text_metar_raw(icao: str) -> str | None:
    """Fetch the raw coded METAR line for a station from NOAA's public text
    mirror. This carries some stations (e.g. YSWS) that AWC's JSON endpoint
    doesn't have yet, since it mirrors the same GTS network more broadly."""
    url = _TEXT_METAR_URL.format(icao=icao)
    req = Request(url, headers={"User-Agent": "AirTrack-ATC/1.0 (metars page)"})
    try:
        with urlopen(req, timeout=_TEXT_METAR_TIMEOUT) as resp:
            text = resp.read().decode("utf-8", errors="replace")
    except (URLError, TimeoutError, OSError):
        return None

    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if len(lines) >= 2 and lines[1].startswith(icao):
        return {"raw": lines[1], "date": lines[0]}
    return None


def _parse_metar_text(raw: str) -> dict:
    """Minimal coded-METAR tokenizer, tuned to the AUTO METAR format used
    by Australian AWS stations. Best-effort: unknown tokens are ignored
    rather than raising, since we'd rather show partial data than none."""
    tokens = raw.strip().split()
    idx = 0
    if idx < len(tokens) and tokens[idx] in ("METAR", "SPECI"):
        idx += 1
    idx += 1  # station ID, already known by caller

    zulu = ""
    if idx < len(tokens) and re.match(r"^\d{6}Z$", tokens[idx]):
        zulu = tokens[idx]
        idx += 1
    if idx < len(tokens) and tokens[idx] in ("AUTO", "COR"):
        idx += 1

    wind_dir_deg = None
    wind_kt = 0
    gust_kt = 0
    if idx < len(tokens):
        m = _WIND_RE.match(tokens[idx])
        if m:
            d, spd, gust, unit = m.groups()
            wind_dir_deg = None if d == "VRB" else int(d)
            wind_kt = int(spd)
            gust_kt = int(gust) if gust else 0
            if unit == "MPS":
                wind_kt = round(wind_kt * _MPS_TO_KT)
                gust_kt = round(gust_kt * _MPS_TO_KT) if gust_kt else 0
            idx += 1
    if idx < len(tokens) and re.match(r"^\d{3}V\d{3}$", tokens[idx]):
        idx += 1

    visib_m = None
    visib_sm = None
    if idx < len(tokens):
        tok = tokens[idx]
        if re.match(r"^\d{4}$", tok):
            visib_m = int(tok)
            idx += 1
        else:
            msm = re.match(r"^(\d+)SM$", tok)
            if msm:
                visib_sm = float(msm.group(1))
                idx += 1

    while idx < len(tokens) and re.match(r"^R\d{2}[LRC]?/", tokens[idx]):
        idx += 1

    wx_codes = []
    while idx < len(tokens):
        tok = tokens[idx]
        if tok in ("SKC", "CLR", "NCD", "NSC") or _CLOUD_RE.match(tok):
            break
        if _TEMP_RE.match(tok) or re.match(r"^Q\d{4}$", tok) or re.match(r"^A\d{4}$", tok):
            break
        wx_codes.append(tok)
        idx += 1

    clouds = []
    sky_clear = False
    while idx < len(tokens):
        tok = tokens[idx]
        if tok in ("SKC", "CLR", "NCD", "NSC"):
            sky_clear = True
            idx += 1
            continue
        m2 = _CLOUD_RE.match(tok)
        if m2:
            cover, base, _ctype = m2.groups()
            clouds.append({"cover": cover, "base_ft": int(base) * 100})
            idx += 1
            continue
        break

    temp_c = None
    dewpoint_c = None
    if idx < len(tokens):
        m3 = _TEMP_RE.match(tokens[idx])
        if m3:
            t, dp = m3.groups()
            temp_c = -int(t[1:]) if t.startswith("M") else int(t)
            if dp:
                dewpoint_c = -int(dp[1:]) if dp.startswith("M") else int(dp)
            idx += 1

    altim_hpa = None
    while idx < len(tokens):
        tok = tokens[idx]
        if tok == "RMK":
            break
        mq = re.match(r"^Q(\d{4})$", tok)
        ma = re.match(r"^A(\d{4})$", tok)
        if mq:
            altim_hpa = int(mq.group(1))
            idx += 1
            break
        if ma:
            altim_hpa = round(int(ma.group(1)) / 100 * 33.8639)
            idx += 1
            break
        idx += 1

    return {
        "zulu": zulu,
        "wind_dir_deg": wind_dir_deg,
        "wind_kt": wind_kt,
        "gust_kt": gust_kt,
        "visib_m": visib_m,
        "visib_sm": visib_sm,
        "wx_codes": [w for w in wx_codes if w != "//"],
        "clouds": clouds,
        "sky_clear": sky_clear,
        "temp_c": temp_c,
        "dewpoint_c": dewpoint_c,
        "altim_hpa": altim_hpa,
    }


def _decode_text(raw_line: str, icao: str) -> dict:
    d = _base_fields(icao)
    reference = None
    if isinstance(raw_line, dict):
        try:
            reference = datetime.strptime(raw_line["date"], "%Y/%m/%d %H:%M").replace(tzinfo=timezone.utc)
        except (ValueError, KeyError):
            pass
        raw_line = raw_line["raw"]
    observed = _text_time(raw_line, reference)
    p = _parse_metar_text(raw_line)

    ceiling_ft = min(
        (c["base_ft"] for c in p["clouds"] if c["cover"] in ("BKN", "OVC", "VV")),
        default=None,
    )
    vis_sm = None
    visib_unlimited = False
    visib_km = None
    if p["visib_m"] is not None:
        visib_unlimited = p["visib_m"] >= 9999
        vis_sm = 10.0 if visib_unlimited else p["visib_m"] * _M_TO_SM
        visib_km = 10.0 if visib_unlimited else round(p["visib_m"] / 1000, 1)
    elif p["visib_sm"] is not None:
        vis_sm = p["visib_sm"]
        visib_km = round(vis_sm * 1.60934, 1)

    flight_cat, flight_cat_color = _classify_flight_category(ceiling_ft, vis_sm)

    cloud_str = ", ".join(f"{c['cover']} {round(c['base_ft'] * 0.3048)} m" for c in p["clouds"])
    if not cloud_str and p["sky_clear"]:
        cloud_str = "Sky clear"

    obs_time = ""
    if p["zulu"]:
        dd, hh, mm = p["zulu"][0:2], p["zulu"][2:4], p["zulu"][4:6]
        obs_time = f"day {dd} · {hh}:{mm} UTC"

    d.update({
        "raw": raw_line,
        "observed_at_utc": observed.isoformat() if observed else None,
        "obs_time": obs_time,
        "source": "TEXT",
        "flight_cat": flight_cat,
        "flight_cat_color": flight_cat_color,
        "temp_c": p["temp_c"],
        "dewpoint_c": p["dewpoint_c"],
        "wind_kmh": round(p["wind_kt"] * _KT_TO_KMH, 1) if p["wind_kt"] else 0,
        "gust_kmh": round(p["gust_kt"] * _KT_TO_KMH, 1) if p["gust_kt"] else 0,
        "wind_dir_compass": _compass(p["wind_dir_deg"]),
        "wind_dir_deg": p["wind_dir_deg"],
        "visib_km": visib_km,
        "visib_unlimited": visib_unlimited,
        "altim_hpa": p["altim_hpa"],
        "wx_string": " ".join(p["wx_codes"]),
        "clouds": cloud_str,
        "ceiling_display": f"{round(ceiling_ft * 0.3048):,} m" if ceiling_ft is not None else ("None" if cloud_str else "—"),
    })
    return d


# ---------------------------------------------------------------------------
# Source 3: BOM observations (last resort — no coded METAR, no flight cat)
# ---------------------------------------------------------------------------

def _fetch_bom_raw(product_id: str, station_id: str) -> dict | None:
    url = _BOM_URL.format(product_id=product_id, station_id=station_id)
    req = Request(url, headers={"User-Agent": "AirTrack-ATC/1.0 (metars page)"})
    try:
        with urlopen(req, timeout=_BOM_TIMEOUT) as resp:
            raw = json.loads(resp.read().decode("utf-8", errors="replace"))
        data = raw.get("observations", {}).get("data", [])
        return data[0] if data else None
    except (URLError, json.JSONDecodeError, TimeoutError, OSError):
        return None


def _format_bom_time(local_date_time_full: str | None) -> str:
    if not local_date_time_full:
        return ""
    try:
        dt = datetime.strptime(local_date_time_full, "%Y%m%d%H%M%S")
        return dt.strftime("%d %b %H:%M local")
    except ValueError:
        return local_date_time_full


def _decode_bom(obs: dict, icao: str) -> dict:
    d = _base_fields(icao)
    vis_km = obs.get("vis_km")
    weather = obs.get("weather") or ""
    if weather == "-":
        weather = ""

    cloud = obs.get("cloud") or ""
    if cloud == "-":
        cloud = ""
    cloud_base_m = obs.get("cloud_base_m")
    cloud_str = f"{cloud}, base {cloud_base_m} m" if cloud and cloud_base_m else cloud

    observed = None
    try:
        if obs.get("aifstime_utc"):
            observed = datetime.strptime(obs["aifstime_utc"], "%Y%m%d%H%M%S").replace(tzinfo=timezone.utc)
        elif obs.get("local_date_time_full"):
            observed = datetime.strptime(obs["local_date_time_full"], "%Y%m%d%H%M%S").replace(tzinfo=ZoneInfo(_TIMEZONES.get(icao, "Australia/Sydney"))).astimezone(timezone.utc)
    except (ValueError, TypeError):
        pass
    d.update({
        "observed_at_utc": observed.isoformat() if observed else None,
        "name": obs.get("name") or d["name"],
        "obs_time": _format_bom_time(obs.get("local_date_time_full")),
        "source": "BOM",
        "temp_c": obs.get("air_temp"),
        "dewpoint_c": obs.get("dewpt"),
        "wind_kmh": obs.get("wind_spd_kmh") or 0,
        "gust_kmh": obs.get("gust_kmh") or 0,
        "wind_dir_compass": obs.get("wind_dir") or "",
        "wind_dir_deg": _compass_to_deg(obs.get("wind_dir")),
        "visib_km": _to_float(vis_km),
        "visib_unlimited": isinstance(vis_km, str) and vis_km.strip().startswith(">"),
        "altim_hpa": obs.get("press_qnh") or obs.get("press"),
        "wx_string": weather,
        "clouds": cloud_str,
    })
    return d


# ---------------------------------------------------------------------------
# Plain-language summary
# ---------------------------------------------------------------------------

def _plain_wx(wx_string: str) -> str:
    if not wx_string:
        return ""
    seen = []
    for tok in wx_string.split():
        label = _WX_PLAIN.get(tok, tok)
        if label not in seen:
            seen.append(label)
    return ", ".join(seen)


def _narrative_summary(d: dict) -> str:
    cat = d.get("flight_cat")
    wind_kmh = d.get("wind_kmh") or 0
    gust_kmh = d.get("gust_kmh") or 0
    compass = d.get("wind_dir_compass") or ""
    visib = d.get("visib_metric")
    wx_plain = _plain_wx(d.get("wx_string") or "")
    clouds = (d.get("clouds") or "").strip()

    openers = {
        "VFR": "Good flying weather",
        "MVFR": "Marginal conditions",
        "IFR": "Poor conditions — instrument flying required",
        "LIFR": "Very poor conditions — low cloud and/or visibility",
    }
    opener = openers.get(cat, "Current conditions")

    if wind_kmh == 0:
        wind_clause = "winds calm"
    else:
        strength = "a light breeze" if wind_kmh < 15 else "a moderate wind" if wind_kmh < 35 else "strong winds"
        from_clause = f"from the {compass}" if compass else "from a variable direction"
        wind_clause = f"{strength} {from_clause} at {wind_kmh} km/h"
        if gust_kmh and gust_kmh > wind_kmh:
            wind_clause += f", gusting to {gust_kmh} km/h"

    bits = [wind_clause]
    if visib and visib != "—":
        bits.append(f"visibility {visib}")
    if wx_plain:
        bits.append(wx_plain)
    elif clouds and clouds.lower() != "sky clear":
        bits.append(clouds.lower())

    return f"{opener} — {', '.join(bits)}."


# ---------------------------------------------------------------------------
# Runway crosswind
# ---------------------------------------------------------------------------

def _runway_heading(ident: str) -> float:
    m = re.match(r"^(\d{2})[LRC]?$", ident)
    return float(m.group(1)) * 10 if m else 0.0


def _wind_components(runway_heading_deg: float, wind_dir_deg: float, wind_kmh: float) -> tuple[float, float]:
    diff = math.radians((wind_dir_deg - runway_heading_deg) % 360)
    headwind = wind_kmh * math.cos(diff)
    crosswind = wind_kmh * math.sin(diff)
    return headwind, crosswind


def _crosswind_table(icao: str, wind_dir_deg: float | None, wind_kmh: float) -> list[dict]:
    pairs = _RUNWAYS.get(icao)
    if not pairs or wind_dir_deg is None:
        return []
    rows = []
    for end_a, end_b in pairs:
        hdg_a, hdg_b = _runway_heading(end_a), _runway_heading(end_b)
        hw_a, xw_a = _wind_components(hdg_a, wind_dir_deg, wind_kmh)
        hw_b, xw_b = _wind_components(hdg_b, wind_dir_deg, wind_kmh)
        if hw_a >= hw_b:
            active_end, headwind, crosswind = end_a, hw_a, xw_a
        else:
            active_end, headwind, crosswind = end_b, hw_b, xw_b
        abs_x = abs(crosswind)
        color = "#63ff95" if abs_x < 19 else "#ffd65f" if abs_x < 37 else "#ff5f5f"
        rows.append({
            "runway": f"{end_a}/{end_b}",
            "active_end": active_end,
            "headwind_kmh": round(headwind, 1),
            "crosswind_kmh": round(abs_x, 1),
            "crosswind_side": "right" if crosswind >= 0 else "left",
            "color": color,
        })
    rows.sort(key=lambda r: r["crosswind_kmh"])
    return rows


def _label_rotation(bearing_deg: float) -> float:
    """Normalise a bearing to the -90..90 range so text rotated by it never
    ends up upside down."""
    rot = bearing_deg % 360
    if 90 < rot < 270:
        rot -= 180
    return rot


def _wind_compass_svg(icao: str, wind_dir_deg: float | None, wind_kmh: float | None) -> str:
    """Compass rose with the field's full runway layout overlaid at true
    heading, a wind-direction arrow, and a semicircular wind-speed gauge.
    Indicative only — see the runway table's own accuracy note."""
    pairs = _RUNWAYS.get(icao, [])

    def pt(cx, cy, radius, bearing_deg):
        rad = math.radians(bearing_deg)
        return cx + radius * math.sin(rad), cy - radius * math.cos(rad)

    cx, cy, r = 150, 155, 128
    parts = ['<svg viewBox="0 0 560 300" width="560" height="300" preserveAspectRatio="xMidYMid meet" class="metar-wind-compass" xmlns="http://www.w3.org/2000/svg">']
    defs_idx = len(parts)

    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#3a4b63" stroke-width="1.5"/>')
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r - 14}" fill="none" stroke="#2a3648" stroke-width="1"/>')

    cardinals = {0: "N", 90: "E", 180: "S", 270: "W"}
    for i in range(12):
        deg = i * 30
        x1, y1 = pt(cx, cy, r, deg)
        x2, y2 = pt(cx, cy, r - 8, deg)
        parts.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#3a4b63" stroke-width="1.5"/>')
        lx, ly = pt(cx, cy, r - 24, deg)
        if deg in cardinals:
            parts.append(f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle" dominant-baseline="middle" fill="#8fa2bd" font-size="16" font-weight="700">{cardinals[deg]}</text>')
        else:
            parts.append(f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle" dominant-baseline="middle" fill="#5c6f8a" font-size="11">{deg // 10}</text>')

    # Runway strips, overlaid at true heading. Near-parallel pairs (e.g.
    # 16L/34R and 16R/34L, which share ~the same simplified heading) are
    # nudged sideways so they render as distinct strips instead of stacking
    # exactly on top of one another and garbling both labels.
    heading_groups: dict[int, list] = {}
    for end_a, end_b in pairs:
        hdg = _runway_heading(end_a)
        bucket = round(hdg / 5) * 5 % 180
        heading_groups.setdefault(bucket, []).append((end_a, end_b, hdg))

    for members in heading_groups.values():
        n = len(members)
        spacing = 20
        offsets = [(-(n - 1) / 2 + i) * spacing for i in range(n)]
        for (end_a, end_b, hdg), offset in zip(members, offsets):
            perp = hdg + 90
            ox = cx + offset * math.sin(math.radians(perp))
            oy = cy - offset * math.cos(math.radians(perp))
            half_len = r * 0.68
            x1, y1 = pt(ox, oy, half_len, hdg)
            x2, y2 = pt(ox, oy, half_len, hdg + 180)
            width = 10
            dx = math.sin(math.radians(perp)) * width / 2
            dy = -math.cos(math.radians(perp)) * width / 2
            poly = f"{x1+dx:.1f},{y1+dy:.1f} {x2+dx:.1f},{y2+dy:.1f} {x2-dx:.1f},{y2-dy:.1f} {x1-dx:.1f},{y1-dy:.1f}"
            parts.append(f'<polygon points="{poly}" fill="#0d1420" stroke="#1c2636" stroke-width="1"/>')
            parts.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#fff" stroke-width="1.5" stroke-dasharray="6 5" opacity="0.85"/>')
            for ex, ey in ((x1, y1), (x2, y2)):
                parts.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="2.5" fill="#fff" opacity="0.9"/>')
            lx1, ly1 = pt(ox, oy, half_len - 14, hdg)
            lx2, ly2 = pt(ox, oy, half_len - 14, hdg + 180)
            rot1, rot2 = _label_rotation(hdg), _label_rotation(hdg + 180)
            parts.append(f'<text x="{lx1:.1f}" y="{ly1:.1f}" text-anchor="middle" dominant-baseline="middle" fill="#fff" font-size="9" font-weight="700" transform="rotate({rot1:.0f} {lx1:.1f} {ly1:.1f})">{end_a}</text>')
            parts.append(f'<text x="{lx2:.1f}" y="{ly2:.1f}" text-anchor="middle" dominant-baseline="middle" fill="#fff" font-size="9" font-weight="700" transform="rotate({rot2:.0f} {lx2:.1f} {ly2:.1f})">{end_b}</text>')

    # Wind direction arrow — points from the direction the wind is coming
    # from, in toward the field.
    if wind_dir_deg is not None and (wind_kmh or 0) > 0:
        tail_x, tail_y = pt(cx, cy, r - 4, wind_dir_deg)
        head_x, head_y = pt(cx, cy, 34, wind_dir_deg)
        parts.insert(defs_idx, (
            '<defs><marker id="windhead" markerWidth="10" markerHeight="10" refX="5" refY="5" '
            'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 L3,5 Z" fill="#63d4ff"/></marker></defs>'
        ))
        parts.append(
            f'<line x1="{tail_x:.1f}" y1="{tail_y:.1f}" x2="{head_x:.1f}" y2="{head_y:.1f}" '
            f'stroke="#63d4ff" stroke-width="4" stroke-linecap="round" marker-end="url(#windhead)"/>'
        )
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="4" fill="#63d4ff"/>')

    # Speedometer — semicircle, 0 at the left sweeping over the top to
    # vmax at the right.
    scx, scy, sr = 420, 180, 108
    vmax = 70
    if wind_kmh and wind_kmh > 55:
        vmax = int(math.ceil((wind_kmh + 10) / 10) * 10)

    def speed_pt(radius, value):
        bearing = -90 + (max(0, min(value, vmax)) / vmax) * 180
        return pt(scx, scy, radius, bearing)

    arc_start = speed_pt(sr, 0)
    arc_end = speed_pt(sr, vmax)
    parts.append(f'<path d="M{arc_start[0]:.1f},{arc_start[1]:.1f} A{sr},{sr} 0 0 1 {arc_end[0]:.1f},{arc_end[1]:.1f}" fill="none" stroke="#3a4b63" stroke-width="2"/>')

    v = 0
    while v <= vmax:
        tx1, ty1 = speed_pt(sr, v)
        tx2, ty2 = speed_pt(sr - 8, v)
        parts.append(f'<line x1="{tx1:.1f}" y1="{ty1:.1f}" x2="{tx2:.1f}" y2="{ty2:.1f}" stroke="#5c6f8a" stroke-width="1.5"/>')
        lx, ly = speed_pt(sr - 22, v)
        parts.append(f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle" dominant-baseline="middle" fill="#8fa2bd" font-size="11">{v}</text>')
        v += 10

    parts.append(f'<text x="{scx}" y="{scy - 34}" text-anchor="middle" fill="#5c6f8a" font-size="12">km/h</text>')

    needle_val = wind_kmh or 0
    nx, ny = speed_pt(sr - 18, needle_val)
    parts.append(f'<line x1="{scx}" y1="{scy}" x2="{nx:.1f}" y2="{ny:.1f}" stroke="#fff" stroke-width="3.5" stroke-linecap="round"/>')
    parts.append(f'<circle cx="{scx}" cy="{scy}" r="8" fill="#0d1420" stroke="#fff" stroke-width="2"/>')
    parts.append(f'<text x="{scx}" y="{scy + 30}" text-anchor="middle" fill="#fff" font-size="18" font-weight="700">{needle_val:.0f}</text>')

    parts.append('</svg>')
    return "".join(parts)


# ---------------------------------------------------------------------------
# Daylight (sunrise/sunset)
# ---------------------------------------------------------------------------

def _daylight_info(icao: str) -> dict | None:
    coords = _COORDS.get(icao)
    if not coords or sun is None:
        return None
    try:
        tzinfo = ZoneInfo(_TIMEZONES.get(icao, "Australia/Sydney"))
        now = datetime.now(tzinfo)
        obs = Observer(latitude=coords[0], longitude=coords[1])
        s_today = sun(obs, date=now.date(), tzinfo=tzinfo)
        sunrise, sunset = s_today["sunrise"], s_today["sunset"]

        if now < sunrise:
            s_prev = sun(obs, date=now.date() - timedelta(days=1), tzinfo=tzinfo)
            span_start, span_end, is_day = s_prev["sunset"], sunrise, False
        elif now > sunset:
            s_next = sun(obs, date=now.date() + timedelta(days=1), tzinfo=tzinfo)
            span_start, span_end, is_day = sunset, s_next["sunrise"], False
        else:
            span_start, span_end, is_day = sunrise, sunset, True

        span = (span_end - span_start).total_seconds()
        pct = max(0.0, min(1.0, (now - span_start).total_seconds() / span)) if span > 0 else 0.0

        return {
            "sunrise": sunrise.strftime("%H:%M"),
            "sunset": sunset.strftime("%H:%M"),
            "now": now.strftime("%H:%M"),
            "is_day": is_day,
            "pct": round(pct * 100, 1),
            "next_event": "sunset" if is_day else "sunrise",
            "next_event_time": span_end.strftime("%H:%M"),
        }
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Trend history (metar_history table)
# ---------------------------------------------------------------------------





def _history_for(icao: str, hours: int = 24) -> list[dict]:
    try:
        conn = _db()
    except Exception:
        return []
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT observed_at, temp_c, wind_kmh, gust_kmh, altim_hpa, flight_cat
                FROM metar_history
                WHERE icao = %s AND observed_at >= (UTC_TIMESTAMP() - INTERVAL %s HOUR)
                ORDER BY observed_at ASC
                """,
                (icao, hours),
            )
            return cur.fetchall()
    except Exception:
        return []
    finally:
        conn.close()


def _sparkline_svg(values: list, width: int = 260, height: int = 46, color: str = "#6dffb1") -> str:
    known = [v for v in values if v is not None]
    if len(known) < 2:
        return ""
    lo, hi = min(known), max(known)
    span = (hi - lo) or 1.0
    step = width / (len(values) - 1) if len(values) > 1 else width
    coords = []
    for i, v in enumerate(values):
        if v is None:
            continue
        x = round(i * step, 1)
        y = round(height - ((v - lo) / span) * (height - 6) - 3, 1)
        coords.append(f"{x},{y}")
    if len(coords) < 2:
        return ""
    points = " ".join(coords)
    last_x, last_y = coords[-1].split(",")
    return (
        f'<svg viewBox="0 0 {width} {height}" preserveAspectRatio="none" class="metar-spark">'
        f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="2" '
        f'stroke-linejoin="round" stroke-linecap="round" vector-effect="non-scaling-stroke"/>'
        f'<circle cx="{last_x}" cy="{last_y}" r="2.5" fill="{color}"/>'
        f'</svg>'
    )


def _trend_block(icao: str) -> dict:
    rows = _history_for(icao, hours=24)
    if len(rows) < 2:
        return {"available": False, "count": len(rows)}
    temps = [r.get("temp_c") for r in rows]
    winds = [r.get("wind_kmh") for r in rows]
    known_temps = [t for t in temps if t is not None]
    known_winds = [w for w in winds if w is not None]
    span_hours = (rows[-1]["observed_at"] - rows[0]["observed_at"]).total_seconds() / 3600
    return {
        "available": True,
        "count": len(rows),
        "span_hours": round(span_hours, 1),
        "temp_svg": _sparkline_svg(temps, color="#ffd65f"),
        "wind_svg": _sparkline_svg(winds, color="#7fb7ff"),
        "temp_min": min(known_temps) if known_temps else None,
        "temp_max": max(known_temps) if known_temps else None,
        "wind_max": max(known_winds) if known_winds else None,
    }


# ---------------------------------------------------------------------------
# Enrichment — adds the dashboard fields to a decoded record, regardless of
# which of the three sources produced it.
# ---------------------------------------------------------------------------

def _airport_name(icao, fallback):
    try:
        conn = _db()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT AirportName FROM airports WHERE ICAO = %s LIMIT 1", (icao,))
                row = cur.fetchone()
                if row and row.get("AirportName"):
                    return row["AirportName"]
        finally:
            conn.close()
    except Exception:
        pass
    return fallback or icao


def _enrich(d: dict, icao: str) -> dict:
    d["airport_name"] = _airport_name(icao, d.get("name"))
    d["runway_layout_known"] = bool(_RUNWAYS.get(icao))
    visib_km = d.get("visib_km")
    if d.get("visib_unlimited"):
        d["visib_metric"] = "10 km+"
    elif visib_km is not None:
        d["visib_metric"] = f"{visib_km:.1f} km"
    else:
        d["visib_metric"] = "—"
    d["summary"] = _narrative_summary(d)
    d["fc_meaning"] = _FC_MEANINGS.get(d.get("flight_cat"), "")
    d["runways"] = _crosswind_table(icao, d.get("wind_dir_deg"), d.get("wind_kmh") or 0)
    d["wind_compass_svg"] = _wind_compass_svg(icao, d.get("wind_dir_deg"), d.get("wind_kmh") or 0)
    d["daylight"] = _daylight_info(icao)
    d["trend"] = _trend_block(icao)
    d["glossary"] = _GLOSSARY
    d["wind_gauge_pct"] = round(min(100.0, (d.get("wind_kmh") or 0) / 60 * 100), 1)
    d["visib_gauge_pct"] = round(min(100.0, (visib_km / 10) * 100), 1) if visib_km is not None else None
    return d


# ---------------------------------------------------------------------------
# Background poller — keeps metar_history populated even when nobody's
# looking at the page, so the trend sparklines have something to show.
# ---------------------------------------------------------------------------





# ---------------------------------------------------------------------------
# Combined fetch (AWC -> NOAA text -> BOM), cached
# ---------------------------------------------------------------------------

def _fetch_and_decode(icao: str, force: bool = False) -> dict | None:
    cached = _cache.get(icao)
    if not force and cached and (time.time() - cached[0]) < _CACHE_TTL:
        return _freshness(cached[1])
    candidates = []
    awc = _fetch_awc_raw(icao)
    if awc:
        candidates.append(_decode_awc(awc, icao))
    if not candidates or not _freshness(candidates[-1])["is_current"]:
        text = _fetch_text_metar_raw(icao)
        if text:
            candidates.append(_decode_text(text, icao))
    if (not candidates or not _freshness(candidates[-1])["is_current"]) and icao in _BOM_STATIONS:
        bom = _fetch_bom_raw(*_BOM_STATIONS[icao])
        if bom:
            candidates.append(_decode_bom(bom, icao))
    decoded = next((d for d in candidates if _freshness(d)["is_current"]), candidates[0] if candidates else None)
    if decoded:
        _enrich(decoded, icao)
        _freshness(decoded)
    _cache[icao] = (time.time(), decoded)
    return decoded


# ---------------------------------------------------------------------------
# Station picker API — search the master airports table and read/write the
# shared 'metar_stations' setting directly (same table + same setting the
# Logbook admin panel's picker uses; see AirTrack-Logbook/app/routes/
# airports_routes.py:search() and admin_routes.py:update_app_settings()).
# ATC and Logbook both connect straight to the same MariaDB instance, so no
# cross-host API call is needed here — just mirror the same SQL.
# ---------------------------------------------------------------------------





@metars_bp.route("/")
@metars_bp.route("/<icao>")
def metars(icao=None):
    stations = _load_stations()
    selected = icao.strip().upper() if icao else None

    if selected and selected not in stations:
        abort(404)

    metar = _fetch_and_decode(selected) if selected else None
    embed = request.args.get("embed") == "1"

    return render_template(
        "metars.html",
        stations=stations,
        selected=selected,
        metar=metar,
        embed=embed,
        selected_theme=get_current_theme(),
        max_age_hours=_MAX_OBSERVATION_AGE / 3600,
    )


