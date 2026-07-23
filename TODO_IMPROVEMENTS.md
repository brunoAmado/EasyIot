# EasyIot - To Do

Created by: Alexandru Hauzman  
Updated: 16.02.2026  
Current version: 9.17-dev

## Important Notes

- Track active work in Backlog.
- Move completed items to Done.

# Backlog

## Firmware & Versioning (P1)

## Security & OTA (P1)

1. [ ] (Blocked) Remove temporary CloudIO HTTP fallback after full TLS compatibility is confirmed on devices (including weak-signal scenarios). File: `src/CloudIO.cpp`
2. [ ] (Blocked - no boards available) Validate OTA update flow over HTTPS on remaining device variants (ESP32 / ESP32C3 / HAN). File: `src/WebServer.cpp`

## Webpanel UX (P1/P2)

## Features & Actuators (P1)

1. [/] Prototype a native non-blocking `LIGHT_DIMMER` actuator driver with push-button hold-to-dim logic, PWM outputs, and web panel range slider integration. Files: `include/Actuatores.h`, `src/Actuatores.cpp`, `webpanel/js/index.js`

## Testing & CI (P2 - Deferred / Later)

- Deferred by owner for now (no Git CI setup in current phase).
1. [ ] (Deferred) Add CI build checks for main envs (ESP8266 + ESP32).
2. [ ] (Deferred) Add smoke tests for boot, Wi-Fi, MQTT, OTA update path.
3. [ ] (Deferred) Add quick rollback notes for failed release/update.
4. [ ] (Deferred) Add CI checks for formatting/sanity of `platformio.ini` (flags, env inheritance, unsafe defaults).

#

# Done

## Build & Version

1. [x] Added support for `platformio_override.ini` local overrides.
2. [x] Added `wifi_flags` injection via `${extra.wifi_flags}`.
3. [x] Updated firmware version format support (example: `9.17-dev`).
4. [x] Updated code/version reporting to use string `VERSION`.
5. [x] Improved `extra_script.py` handling for quoted `VERSION` values.
6. [x] Added `CHANGELOG.md` as the single release-history file.
7. [x] Added pre-release metadata validator (version/changelog/env/OTA URL checks). File: `tools/validate_release.sh`
8. [x] Added automatic pre-build hooks for HTML conversion and release validation with skip flags. Files: `tools/extra_script.py`, `platformio.ini`
9. [x] Enforced `WEB_SECURE_ON` for production/non-debug profiles and removed debug defaults from release builds. File: `platformio.ini`
10. [x] Automated webpanel asset cache version (`?v=`) from project version during build conversion (no manual hardcoded value updates). Files: `webpanel/index.html`, `tools/html_converter.sh`

## Security

1. [x] Stopped logging credential values in debug output (`src/CoreWiFi.cpp`, `src/ConfigOnofre.cpp`).
2. [x] Validated OTA update flow over HTTPS on ESP32 (`Update Success` + reboot + reconnect to CloudIO/MQTT; `HTTPS result: 200`, `fallback=0`). File: `src/WebServer.cpp`
3. [x] Converted state-changing endpoints to support `POST` (`/reboot`, `/load-defaults`, `/templates/change`) and switched webpanel calls to `POST` while keeping temporary `GET` compatibility. Files: `src/WebServer.cpp`, `webpanel/js/index.js`
4. [x] Implemented HTTPS-first config sync for CloudIO with silent HTTP fallback after 3 retries. File: `src/CloudIO.cpp`
5. [x] Hardened captive portal Wi-Fi configuration flow to submit SSID and password via `POST` body instead of `GET` query parameters. Files: `include/CaptivePortal.h`, `src/WebServer.cpp`

## Webpanel

1. [x] Fixed firmware version comparison for `-dev` formats (replaced `parseFloat` logic). File: `webpanel/js/index.js`
2. [x] Removed hardcoded `baseUrl` and switched to same-origin requests. File: `webpanel/js/index.js`
3. [x] Added automatic firmware version display in webpanel footer (`version_lbl` from `/config`). Files: `webpanel/index.html`, `webpanel/js/index.js`
4. [x] Added firmware build date to `/config` API payload and system log output. Files: `src/ConfigOnofre.cpp`, `src/WebServer.cpp`
5. [x] Prototyped a native non-blocking `LIGHT_DIMMER` actuator driver with push-button hold-to-dim logic, PWM outputs, and web panel range slider integration. Files: `include/Actuatores.h`, `src/Actuatores.cpp`, `webpanel/js/index.js`

## Code Quality

1. [x] Replaced deprecated ArduinoJson `containsKey()` checks in config update path with `isNull()` guards. File: `src/ConfigOnofre.cpp`
2. [x] Added explicit ESP8266 no-op switch cases for ESP32-only sensor drivers (`TMF882X`, `LD2410`, `LD2450`, `LD2460`) to remove compiler switch warnings. File: `src/Sensors.cpp`

## Process & Release

1. [x] Added PR workflow guide (development -> cherry-pick branch -> upstream PR). File: `docs/RELEASE_WORKFLOW.md`
2. [x] Added branch naming convention for external CP branches. File: `docs/RELEASE_WORKFLOW.md`
3. [x] Added release checklist document in repo docs. File: `docs/RELEASE_WORKFLOW.md`
4. [x] Added script to generate release notes draft from commits. File: `tools/generate_release_notes.sh`

## Testing & CI

1. [x] Added GitHub Actions CI build checks for main environments (ESP8266 + ESP32) to compile on pull request or push. File: `.github/workflows/ci.yml`
2. [x] Added smoke testing manual verification checklist covering boot diagnostics, Wi-Fi, MQTT, and OTA paths. File: `docs/smoke_test_guide.md`
3. [x] Added quick rollback recovery notes and esptool wipe instructions for failed release/update. File: `docs/ROLLBACK_NOTES.md`

## Quick Release Flow

1. Bump version in `platformio.ini`.
2. Build target environments.
3. Validate OTA and displayed firmware version.
4. Commit and push changes.
5. Open PR and release notes.
