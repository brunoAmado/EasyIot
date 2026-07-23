# Config Constants & Backlog

> 15 nodes

## Key Concepts

- **Shutters.cpp** (14 connections) — `src/Shutters.cpp`
- **_operationHandler** (4 connections) — `include/Shutters.h`
- **Shutters::_halt()** (3 connections) — `src/Shutters.cpp`
- **_setSafetyDelay** (2 connections) — `include/Shutters.h`
- **Shutters::_up()** (2 connections) — `src/Shutters.cpp`
- **Shutters::_down()** (2 connections) — `src/Shutters.cpp`
- **Shutters::Shutters()** (1 connections) — `src/Shutters.cpp`
- **Shutters::_setSafetyDelay()** (1 connections) — `src/Shutters.cpp`
- **Shutters::getUpCourseTime()** (1 connections) — `src/Shutters.cpp`
- **Shutters::getDownCourseTime()** (1 connections) — `src/Shutters.cpp`
- **Shutters::getCalibrationRatio()** (1 connections) — `src/Shutters.cpp`
- **Shutters::isIdle()** (1 connections) — `src/Shutters.cpp`
- **Shutters::isCalibration()** (1 connections) — `src/Shutters.cpp`
- **Shutters::getCurrentLevel()** (1 connections) — `src/Shutters.cpp`
- **Shutters::isReset()** (1 connections) — `src/Shutters.cpp`

## Relationships

- [Hardware Configuration Profiles](Hardware_Configuration_Profiles.md) (2 shared connections)
- [CloudIO & MQTT Declarations](CloudIO_&_MQTT_Declarations.md) (1 shared connections)
- [Family Constants](Family_Constants.md) (1 shared connections)

## Source Files

- `include/Shutters.h`
- `src/Shutters.cpp`

## Audit Trail

- EXTRACTED: 28 (78%)
- INFERRED: 8 (22%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*