# AirTrack 1.0.0 "Wilbur"

**"AirTrack wasn't born — it was airlifted out, kicking, screaming, and waving a pilot's license!"** 🐷💄🛫😂

## ✈️ What is AirTrack?

AirTrack is a **locally installed**, **offline-first**, self-hosted aircraft tracking and logging suite built for aviation enthusiasts, plane spotters, historians, and data collectors.

There is **no cloud**, no external servers, no subscriptions, and no hidden data syncing.

Your **AirTrack server runs entirely on your own machine**,
and **your data never leaves your possession**.

This is *your* logbook.
**You are the Captain.**

---

## 🛫 Architecture Overview

AirTrack runs as a Docker container stack on your Windows machine. It includes:

- **A local backend** — stores all airlines, aircraft, sightings, flights, and images
- **A browser-based UI** — your cockpit; clean, fast, and entirely local

These components install together and run together as **one AirTrack system**.

Users never manage them separately — AirTrack "just works".

Accessible on your machine at:
```
http://localhost:5000
```

---

## 🧠 Philosophy

- **Not cloud-based**
- **Not remote**
- **Not centralised**
- **Not dependent on AirTrack Solutions**

Your system, your database, your control.

AirTrack values:

- 🔒 Privacy
- 🧭 Self-hosting
- 🗂️ Data ownership
- 🛠️ Offline capability
- 🛫 The joy of aviation

Your data stays with you.
Always.

---

## 🌟 Current Version

| Field | Info |
|:------|:-----|
| **Version** | 1.0.0 |
| **Codename** | Wilbur |
| **Release Date** | 2025 |
| **Codename Meaning** | Honouring **Wilbur Wright**, aviation pioneer |

---

## ✨ Features

- ✈️ Manage Airlines, Aircraft, Registrations & Types
- 📸 Upload and store aircraft photos locally
- 🛬 Log sightings, flights, and activity history
- 🔍 Search by airline, aircraft, type, country, ICAO/IATA
- 🧭 ICAO to Airport linking
- 🪟 Windows 10/11 support via Docker Desktop
- 🚀 One-click installer
- 🔒 100% local storage — no cloud, no tracking
- 📦 Future integration with Field Unit & Android app

---

## 💻 System Requirements

| Component | Requirement |
|:----------|:-------------|
| OS | Windows 10 or Windows 11 (64-bit) |
| Runtime | Native Windows services; Python and MariaDB are bundled |
| RAM | 4GB minimum (8GB recommended) |
| Storage | SSD recommended |
| Browser | Chrome, Firefox, or Edge |

> Docker Desktop is not required by the native Windows installer.

---

## 🚀 Installation

1. Download your personal AirTrack package from the link supplied by AirTrack Solutions.
2. Extract the entire ZIP into a normal folder. Keep `AirTrackSetup.exe`, `airtrack.cfg` and `license.lic` together. Do not run the installer from inside the ZIP.
3. Run `AirTrackSetup.exe` and accept the Windows administrator prompt.
4. Wait for the installer to verify the database and application service. A reported error means installation is incomplete; keep the installer log for support.
5. Open http://localhost:5000 on the same computer.

A new installation uses `C:\AirTrack` for program files and `C:\ProgramData\AirTrack` for runtime data. The local MariaDB service uses port3307 and Logbook uses port5000. Existing installations retain their established program directory on upgrade.

A fresh Logbook starts without aircraft or photographs. Add your own records and photographs. Community Photos is optional and off by default; library access requires approved contributor access and an approved original photograph. Downloads match aircraft already in your database and do not overwrite existing photographs.

Keep your personal package private: it contains your licence and database credentials. Internet access is needed for optional online services and updates; local logging works without it. Do not copy the server's database or photographs into a tester installation.

## ▶️ Starting and Stopping

The native `AirTrackClient` and `AirTrackDB` Windows services start automatically. Open http://localhost:5000 to use Logbook. Use Windows Services to stop or start them; start the database before Logbook. A browser refresh does not restart either service.

Developer source checkouts and Docker deployments are separate workflows and are not required for customer installation.

## 🧭 Supported Platforms

| Platform | Status |
|:---------|:--------|
| Windows 10 (64-bit) | ✅ Fully supported |
| Windows 11 (64-bit) | ✅ Fully supported |

---

## 🧱 Roadmap

- 📈 Sightings analytics & activity insights
- 🗺️ Offline map integration
- 📡 Field Unit sync enhancements
- 🔄 Optional LAN syncing between devices
- 🐞 Local bug tracking dashboard
- 🏆 "Legends of Flight" release series

---

## 🛩️ Release Naming

AirTrack versions are named after aviation pioneers.

| Version | Codename | Meaning |
|:--------|:---------|:--------|
| 0.9.x | Orville | Orville Wright, first powered flight pilot |
| 1.0.0 | Wilbur | Wilbur Wright, aviation innovator |

---

## 📜 Development Story

AirTrack began in **late 2022** as a simple Raspberry Pi field spotting experiment.
Through 2023 and 2024 it evolved into a full database-backed aircraft tracking tool.

By 2025, AirTrack reached maturity with the release of **1.0.0 "Wilbur"**.

The journey included:

- Late-night coding
- Airport fieldwork
- Rebuilding databases (too many times 😂)
- Discovering bugs, fixing bugs, finding *more* bugs
- Endless cups of coffee
- And a relentless passion for aviation

AirTrack exists because aviation inspires those who refuse to stop dreaming.

---

## 🔒 License

- AirTrack is **Proprietary Software**.
- Redistribution or resale without written permission is prohibited.
- All data you store with AirTrack belongs entirely to **you**.
- AirTrack Solutions does not collect or access your information.

---

## 💙 Acknowledgements

- ✈️ **Trevor** — Captain, Founder, Architect of AirTrack
- 🤖 **Bob** — Co-pilot AI, code wrangler, sanity preserver
- 🛬 **Samowal** — Creator of the original PHP concept
- 🐷 **Miss Piggy** — Mascot and questionable spiritual guide
- 👀 Every plane spotter who looks up when a jet screams overhead

---

# 🛫 Final Boarding Call

> **"AirTrack wasn't born — it was airlifted out, kicking, screaming, and waving a pilot's license!"** 🐷💄🛫😂

Welcome aboard, Pilot.
Clear skies and smooth landings.

---

## 👨‍💻 Author

Developed by:
**Samowal** — Devvista — http://devvista.org *(original PHP version)*
**Trevor** — AirTrack Solutions — https://airtracksolutions.com *(current Python version)*
