# AirTrack 1.0.0
# Copyright (c) 2025 Trevor (“Subhuti”). All rights reserved.
# SPDX-License-Identifier: LicenseRef-AirTrack-Proprietary-NC



# Auto-generated AirTrack version module

import json
import re
import sys
from pathlib import Path

# The installer ships this identity with every frozen application release.
_assets = Path(sys._MEIPASS) / 'app' if getattr(sys, 'frozen', False) else Path(__file__).resolve().parent
AIRTRACK_VERSION = json.loads((_assets / 'windows_release.json').read_text(encoding='utf-8'))['version']
if not isinstance(AIRTRACK_VERSION, str) or not re.fullmatch(r'\d+\.\d+\.\d+', AIRTRACK_VERSION):
    raise ValueError('Invalid installed Windows release version')
# One semantic version identifies the application and its visible label.
FULL_VERSION = AIRTRACK_VERSION
SHORT_VERSION = AIRTRACK_VERSION
DISPLAY_VERSION = f"AirTrack Logbook {AIRTRACK_VERSION}"
