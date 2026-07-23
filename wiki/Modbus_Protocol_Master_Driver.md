# Modbus Protocol Master Driver

> 39 nodes

## Key Concepts

- **WebServer.cpp** (16 connections) — `src/WebServer.cpp`
- **CoreWiFi.cpp** (15 connections) — `src/CoreWiFi.cpp`
- **checkInternalRoutines()** (7 connections) — `src/main.cpp`
- **infoCallback()** (6 connections) — `src/CoreWiFi.cpp`
- **SysProvEvent()** (5 connections) — `src/CoreWiFi.cpp`
- **setupWiFi()** (5 connections) — `src/CoreWiFi.cpp`
- **loadAPI()** (5 connections) — `src/WebServer.cpp`
- **setupWebPanel()** (5 connections) — `src/WebServer.cpp`
- **main.cpp** (5 connections) — `src/main.cpp`
- **setup()** (5 connections) — `src/main.cpp`
- **loop()** (5 connections) — `src/main.cpp`
- **getApName()** (4 connections) — `src/CoreWiFi.cpp`
- **reloadWiFiConfig()** (4 connections) — `src/CoreWiFi.cpp`
- **scanNewWifiNetworks()** (3 connections) — `src/CoreWiFi.cpp`
- **mdnsCallback()** (3 connections) — `src/CoreWiFi.cpp`
- **refreshMDNS()** (3 connections) — `src/CoreWiFi.cpp`
- **loopWiFi()** (3 connections) — `src/CoreWiFi.cpp`
- **stopWebserver()** (3 connections) — `src/WebServer.cpp`
- **startWebserver()** (3 connections) — `src/WebServer.cpp`
- **infoWifi()** (2 connections) — `src/CoreWiFi.cpp`
- **dissableAP()** (2 connections) — `src/CoreWiFi.cpp`
- **justwifi_messages_t** (2 connections)
- **beginBleProvison()** (2 connections) — `src/CoreWiFi.cpp`
- **performUpdate()** (2 connections) — `src/WebServer.cpp`
- **errorResponse()** (2 connections) — `src/WebServer.cpp`
- *... and 14 more nodes in this community*

## Relationships

- [Hardware Access & Sensor Drivers](Hardware_Access_&_Sensor_Drivers.md) (6 shared connections)
- [CloudIO MQTT Integration](CloudIO_MQTT_Integration.md) (2 shared connections)
- [Shutter Calibration & Math](Shutter_Calibration_&_Math.md) (1 shared connections)
- [Utility Binary Operations](Utility_Binary_Operations.md) (1 shared connections)

## Source Files

- `include/CaptivePortal.h`
- `include/IndexHtml.h`
- `include/IndexJs.h`
- `include/StylesMinCss.h`
- `src/CoreWiFi.cpp`
- `src/WebServer.cpp`
- `src/main.cpp`

## Audit Trail

- EXTRACTED: 104 (76%)
- INFERRED: 32 (24%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*