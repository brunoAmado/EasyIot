# Web Panel Frontend & Templates

> 49 nodes

## Key Concepts

- **Actuator** (50 connections) — `include/Actuatores.h`
- **Actuator::changeState()** (11 connections) — `src/Actuatores.cpp`
- **Actuator::setup()** (9 connections) — `src/Actuatores.cpp`
- **.familyToText()** (7 connections) — `include/Actuatores.h`
- **.findDriver()** (7 connections) — `include/Actuatores.h`
- **.isCover()** (5 connections) — `include/Actuatores.h`
- **.isLight()** (5 connections) — `include/Actuatores.h`
- **.isSwitch()** (5 connections) — `include/Actuatores.h`
- **.isGarage()** (5 connections) — `include/Actuatores.h`
- **.isGardenValve()** (4 connections) — `include/Actuatores.h`
- **.isKnxSupport()** (4 connections) — `include/Actuatores.h`
- **writeToPIN()** (4 connections) — `src/Utils.cpp`
- **ActuatorDriver** (3 connections)
- **String** (3 connections)
- **.findDriverFromName()** (3 connections) — `include/Actuatores.h`
- **.isRelay()** (2 connections) — `include/Actuatores.h`
- **.isKnxGroup()** (2 connections) — `include/Actuatores.h`
- **.requireDualInputs()** (2 connections) — `include/Actuatores.h`
- **.driverToText()** (2 connections) — `include/Actuatores.h`
- **.driverToInputMode()** (2 connections) — `include/Actuatores.h`
- **ActuatorInputMode** (2 connections)
- **setup** (2 connections) — `include/Actuatores.h`
- **StateOrigin** (2 connections)
- **uniqueId** (1 connections) — `include/Actuatores.h`
- **name** (1 connections) — `include/Actuatores.h`
- *... and 24 more nodes in this community*

## Relationships

- [Hardware Access & Sensor Drivers](Hardware_Access_&_Sensor_Drivers.md) (5 shared connections)
- [Shutter Calibration & Math](Shutter_Calibration_&_Math.md) (4 shared connections)
- [CloudIO & MQTT Declarations](CloudIO_&_MQTT_Declarations.md) (3 shared connections)
- [CloudIO MQTT Integration](CloudIO_MQTT_Integration.md) (2 shared connections)
- [Utility Binary Operations](Utility_Binary_Operations.md) (2 shared connections)
- [Device Components & Core Headers](Device_Components_&_Core_Headers.md) (1 shared connections)

## Source Files

- `include/Actuatores.h`
- `src/Actuatores.cpp`
- `src/Utils.cpp`

## Audit Trail

- EXTRACTED: 131 (78%)
- INFERRED: 36 (22%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*