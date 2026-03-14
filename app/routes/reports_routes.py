# AirTrack 1.0.0
# Copyright (c) 2025 Trevor (“Subhuti”). All rights reserved.
# SPDX-License-Identifier: LicenseRef-AirTrack-Proprietary-NC



from datetime import date, datetime

import pytz
from flask import Blueprint, flash, redirect, render_template, request, url_for
from sqlalchemy import text

from extensions import db
from utils.settings_utils import get_current_timezone

reports_bp = Blueprint("reports", __name__, url_prefix="/reports")


# -------------------------------------------------
# Helpers
# -------------------------------------------------
def _to_tz(dt, tz):
    """Normalize dates → datetime and convert UTC → user timezone."""
    if not dt:
        return None
    if isinstance(dt, date) and not isinstance(dt, datetime):
        dt = datetime.combine(dt, datetime.min.time())
    return dt.replace(tzinfo=pytz.utc).astimezone(tz)


def render_report(title, columns, data):
    return render_template(
        "partials/_report_table.html", title=title, columns=columns, data=data
    )


def safe_query(sql, params=None, title="", columns=None):
    """Execute a safe DB query with optional parameters and render a report.

    - Guards against SQL errors
    - Normalizes First_Sighted timestamps
    - Uses UTC→local timezone conversion
    """
    try:
        result = db.session.execute(text(sql), params or {})
        rows = [dict(row._mapping) for row in result.fetchall()]

        timezone = get_current_timezone()
        for row in rows:
            if "First_Sighted" in row:
                dt = row["First_Sighted"]
                converted = _to_tz(dt, timezone)
                row["First_Sighted"] = (
                    converted.strftime("%d-%m-%Y %H:%M:%S") if converted else "Unknown"
                )

        return render_report(title, columns or [], rows)

    except Exception as e:
        print(f"❌ Error in report '{title}': {e}")
        flash("Report failed to generate.", "danger")
        return render_report(title, columns or [], [])


# -------------------------------------------------
# Routes
# -------------------------------------------------
@reports_bp.route("/")
def reports_index():
    """Alias/index that accepts ?report=... or ?report_name=... and redirects."""
    name = (
        request.args.get("report")
        or request.args.get("report_name")
        or "logged_airports"
    )
    routes = {
        "logged_airports": "reports.report_logged_airports",
        "most_seen_aircraft": "reports.most_seen_aircraft",
        "top_airlines": "reports.top_airlines",
        "most_frequent_routes": "reports.most_frequent_routes",
        "top_10_busiest_airports": "reports.top_10_busiest_airports",
        "first_time_sightings": "reports.first_time_sightings",
        "rare_airlines": "reports.rare_airlines",
        "top_countries": "reports.top_countries",
        "most_common_models": "reports.most_common_models",
        "oldest_aircraft": "reports.oldest_aircraft",
        "different_aircraft": "reports.different_aircraft_report",
    }
    endpoint = routes.get(name, "reports.report_logged_airports")
    return redirect(url_for(endpoint))


@reports_bp.route("/logged_airports")
def report_logged_airports():
    try:
        flight_count = db.session.execute(text("SELECT COUNT(*) FROM flights")).scalar()
        if not flight_count:
            flash("No flights found to generate the report.", "info")
            return render_report("Logged Airports", ["ICAO", "AirportName", "Country"], [])

        query = text("""
            SELECT DISTINCT a.ICAO, a.AirportName, a.Country
            FROM airports a
            JOIN (
                SELECT DISTINCT Departure AS ICAO FROM flights
                UNION
                SELECT DISTINCT Arrival AS ICAO FROM flights
            ) f ON a.ICAO = f.ICAO
            WHERE a.AirportName IS NOT NULL AND a.AirportName != ''
            ORDER BY a.Country, a.AirportName
        """)

        with db.engine.connect() as conn:
            result = conn.execute(query)
            columns = result.keys()
            airports = [dict(zip(columns, row)) for row in result]

    except Exception as e:
        import logging
        logging.error(f"❌ Error generating Logged Airports report: {e}")
        flash("Failed to load Logged Airports report.", "danger")
        airports = []

    return render_report("Logged Airports", ["ICAO", "AirportName", "Country"], airports)


@reports_bp.route("/most_seen_aircraft")
def most_seen_aircraft():
    return safe_query(
        """
        SELECT Registration, COUNT(*) AS TimesSeen
        FROM flights
        GROUP BY Registration
        ORDER BY TimesSeen DESC
        LIMIT 20
        """,
        title="Most Seen Aircraft",
        columns=["Registration", "TimesSeen"],
    )


@reports_bp.route("/top_airlines")
def top_airlines():
    return safe_query(
        """
        SELECT a.AirlineName, COUNT(*) AS Flights
        FROM flights f
        LEFT JOIN airlines a ON f.AirlineID = a.AirlineID
        WHERE a.AirlineName IS NOT NULL
        GROUP BY a.AirlineName
        ORDER BY Flights DESC
        LIMIT 20
        """,
        title="Top Airlines",
        columns=["AirlineName", "Flights"],
    )


@reports_bp.route("/most_frequent_routes")
def most_frequent_routes():
    return safe_query(
        """
        SELECT a1.AirportName AS Departure,
               a2.AirportName AS Arrival,
               COUNT(*) AS Flights
        FROM flights f
        INNER JOIN airports a1 ON f.Departure = a1.ICAO
        INNER JOIN airports a2 ON f.Arrival = a2.ICAO
        WHERE a1.AirportName IS NOT NULL AND a1.AirportName != ''
          AND a2.AirportName IS NOT NULL AND a2.AirportName != ''
        GROUP BY f.Departure, f.Arrival
        ORDER BY Flights DESC
        LIMIT 20
        """,
        title="Most Frequent Routes",
        columns=["Departure", "Arrival", "Flights"],
    )


@reports_bp.route("/top_10_busiest_airports")
def top_10_busiest_airports():
    return safe_query(
        """
        SELECT a.AirportName AS Airport, airport_stats.Count
        FROM (
            SELECT Airport, COUNT(*) AS Count
            FROM (
                SELECT Departure AS Airport FROM flights WHERE Departure IS NOT NULL
                UNION ALL
                SELECT Arrival AS Airport FROM flights WHERE Arrival IS NOT NULL
            ) AS Combined
            GROUP BY Airport
        ) AS airport_stats
        INNER JOIN airports a ON airport_stats.Airport = a.ICAO
        WHERE a.AirportName IS NOT NULL AND a.AirportName != ''
        ORDER BY airport_stats.Count DESC
        LIMIT 10
        """,
        title="Top 10 Busiest Airports",
        columns=["Airport", "Count"],
    )


@reports_bp.route("/first_time_sightings")
def first_time_sightings():
    return safe_query(
        """
        SELECT Registration, First_Sighted
        FROM aircraft
        LIMIT 20
        """,
        title="First-Time Sightings",
        columns=["Registration", "First_Sighted"],
    )


@reports_bp.route("/rare_airlines")
def rare_airlines():
    return safe_query(
        """
        SELECT a.AirlineName, COUNT(*) AS Sightings
        FROM flights f
        LEFT JOIN airlines a ON f.AirlineID = a.AirlineID
        GROUP BY a.AirlineName
        HAVING Sightings <= 2
        ORDER BY Sightings ASC
        LIMIT 20
        """,
        title="Rare Airline Sightings",
        columns=["AirlineName", "Sightings"],
    )


@reports_bp.route("/top_countries")
def top_countries():
    return safe_query(
        """
        SELECT Country_of_Reg, COUNT(*) AS Count
        FROM aircraft
        WHERE Country_of_Reg IS NOT NULL AND Country_of_Reg != ''
        GROUP BY Country_of_Reg
        """,
        title="Top Countries of Registration",
        columns=["Country_of_Reg", "Count"],
    )


@reports_bp.route("/most_common_models")
def most_common_models():
    return safe_query(
        """
        SELECT Aircraft_Type, Country_of_Reg, COUNT(*) AS Count
        FROM aircraft
        WHERE Aircraft_Type IS NOT NULL AND Country_of_Reg IS NOT NULL
        GROUP BY Aircraft_Type, Country_of_Reg
        ORDER BY Count DESC
        """,
        title="Most Common Models Per Country",
        columns=["Aircraft_Type", "Country_of_Reg", "Count"],
    )


@reports_bp.route("/oldest_aircraft")
def oldest_aircraft():
    return safe_query(
        """
        SELECT Registration, Aircraft_Type, Manufacture_Year,
               YEAR(CURDATE()) - Manufacture_Year AS Age
        FROM aircraft
        WHERE Manufacture_Year IS NOT NULL AND Manufacture_Year != ''
        ORDER BY Manufacture_Year ASC
        LIMIT 20
        """,
        title="Oldest Aircraft Still in Service",
        columns=["Registration", "Aircraft_Type", "Manufacture_Year", "Age"],
    )


@reports_bp.route("/different_aircraft", methods=["GET"])
def different_aircraft_report():
    return safe_query(
        """
        SELECT Aircraft_Type, COUNT(*) AS Total
        FROM aircraft
        WHERE Aircraft_Type IS NOT NULL AND Aircraft_Type != ''
        GROUP BY Aircraft_Type
        ORDER BY Total DESC
        """,
        title="Different Aircraft Types",
        columns=["Aircraft_Type", "Total"],
    )


@reports_bp.route("/support")
def support():
    return render_template("support.html")

