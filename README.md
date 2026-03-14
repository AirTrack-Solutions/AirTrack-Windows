# AirTrack 1.0.0 "Wilbur"

**"AirTrack wasn't born — it was airlifted out, kicking, screaming, and waving a pilot's license!"** 🐷💄🛫😂

## ✈️ What is AirTrack?

AirTrack is a **locally installed**, **offline-first**, self-hosted aircraft tracking and logging suite built for aviation enthusiasts, plane spotters, historians, and data collectors.

There is **no cloud**, no external servers, no subscriptions, and no hidden data syncing.

Your **AirTrack-server runs entirely on your own machine**,
your **AirTrack-client connects locally**,
and **your data never leaves your possession**.

This is *your* logbook.
**You are the Captain.**

---

## 🛫 Architecture Overview

AirTrack includes two tightly integrated components:

### **1. AirTrack-server (Local Backend)**
- Runs quietly in Docker
- Stores all airlines, aircraft, sightings, flights, and images
- Provides the internal API used by the client
- Accessible on your machine at:
  ```
  http://localhost:5000
  ```

### **2. AirTrack-client (Local UI)**
- A browser-based user interface
- Displays your database in a fast, clean cockpit environment
- Uploads images, manages aircraft, tracks flights
- Interacts only with *your* local server

These components install together and run together as **one AirTrack system**.

Users never manage them separately — AirTrack "just works".

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
- 🧭 ICAO to Airport linking (when available)
- 🐧 Linux & Raspberry Pi support
- 🪟 Windows 10/11 support via Docker Desktop
- 🚀 One-click installer for Linux and Windows
- 🔒 100% local storage — no cloud, no tracking
- 📦 Future integration with Field Unit & Android app

---

## 💻 System Requirements

### Linux / Raspberry Pi

| Component | Requirement |
|:----------|:-------------|
| OS | Linux Desktop (Ubuntu/Pop!_OS/Mint) or Raspberry Pi OS (64-bit) |
| Docker | Installed or installed automatically by the installer |
| Docker Compose | Installed or installed automatically |
| RAM | 2GB minimum |
| Storage | SSD or SD Card |
| Browser | Chrome, Firefox, Edge, or Safari |

### Windows

| Component | Requirement |
|:----------|:-------------|
| OS | Windows 10 or Windows 11 (64-bit) |
| Docker Desktop | Required — installer will prompt if not found |
| RAM | 4GB minimum (8GB recommended) |
| Storage | SSD recommended |
| Browser | Chrome, Firefox, or Edge |

> **Note:** Docker Desktop must be running before launching AirTrack on Windows.

---

## 🚀 Installation

### Linux / Raspberry Pi

1. Download and unzip the AirTrack Installer Package.
2. Open a terminal inside the extracted folder.
3. Make the installer executable:

```bash
chmod +x install_airtrack.sh
```

4. Run the installer:

```bash
./install_airtrack.sh
```

5. When installation completes, open your browser:

```
http://localhost:5000
```

### Windows — Option A: Installer (Recommended)

1. Download the AirTrack Windows Installer (`AirTrack-Windows-Installer.exe`) from [airtracksolutions.com.au](http://airtracksolutions.com.au).
2. Ensure **Docker Desktop** is installed and running.
3. Right-click the installer and select **Run as Administrator**.
4. Follow the prompts — AirTrack will install to:
   ```
   C:\Users\<you>\docker\AirTrack-Windows\
   ```
5. When installation completes, open your browser:
   ```
   http://localhost:5000
   ```

### Windows — Option B: Clone from GitHub

For users comfortable with Docker and PowerShell.

1. Ensure **Docker Desktop** is installed and running.
2. Open PowerShell and clone the repository:
   ```powershell
   git clone https://github.com/Subhuti/AirTrack-Windows.git "%USERPROFILE%\docker\AirTrack-Windows"
   cd "%USERPROFILE%\docker\AirTrack-Windows"
   ```
3. Run the installer script as Administrator:
   ```powershell
   powershell -ExecutionPolicy Bypass -NoProfile -File install_airtrack_windows.ps1
   ```
4. When installation completes, open your browser:
   ```
   http://localhost:5000
   ```

> **To start AirTrack after a reboot**, run `start_airtrack.bat` in your AirTrack-Windows folder, or ensure Docker Desktop starts automatically on login.

You are now flying with AirTrack! 🛫

---

## 🧭 Supported Platforms

| Platform | Status |
|:---------|:--------|
| Linux Desktop (Ubuntu, Mint, Pop!_OS) | ✅ Fully supported |
| Raspberry Pi OS (64-bit) | ✅ Fully supported |
| Debian-based distros | ✅ Should work |
| Windows 10 / 11 via Docker Desktop | ✅ Fully supported |
| macOS via Docker Desktop | 🚧 Planned |

---

## 🧱 Roadmap

- 📈 Sightings analytics & activity insights
- 🗺️ Offline map integration
- 📡 Field Unit sync enhancements
- 🍎 macOS installer package
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
**Trevor** — AirTrack Solutions — http://airtracksolutions.com.au *(current Python version)*
