# EasyIot Developer & Architecture Guide

This guide details the internal software architecture of the EasyIot firmware, outlining the core engines, classes, and how to extend them.

---

## 1. Core Codebase Structure

The firmware is written in C++ using the Arduino framework. The core components are organized as follows:

* **`src/main.cpp`**: Main firmware entry point. Initializes logging, loads configuration, manages the main state loop, and sets up network services.
* **`src/ConfigOnofre.cpp` / `include/ConfigOnofre.h`**: Manages device configuration. Handles loading/saving settings as JSON in the LittleFS filesystem.
* **`src/Actuatores.cpp` / `include/Actuatores.h`**: Implements the actuator class and relay/dimmer drivers (switches, buttons, shutter doors).
* **`src/Sensors.cpp` / `include/Sensors.h`**: Implements the sensor class and interfaces with external environmental and presence hardware.
* **`src/WebServer.cpp` / `include/WebServer.h`**: Configures the asynchronous web server, REST API, Captive Portal, and handles compressed UI assets.
* **`src/HomeAssistantMqttDiscovery.cpp`**: Generates MQTT auto-discovery JSON payloads for Home Assistant entity mapping.
* **`src/Templates.cpp`**: Contains static GPIO profiles for preconfigured hardware boards.

---

## 2. Configuration Engine (`ConfigOnofre`)

All settings (WiFi, MQTT, registered actuators, and sensors) are stored inside the global `config` object of type `ConfigOnofre`:

* **Storage**: Settings are saved in `/config.json` inside the MCU's **LittleFS** flash partition.
* **Serialization**: The class uses `ArduinoJson` to serialize settings to a file (`config.save()`) and deserialize on boot (`config.load()`).
* **Pin Validation**: Includes safety rules (`config.validPin(gpio)`) to prevent users from mapping features onto critical MCU pins (e.g. flash pins, hardware serial pins).

---

## 3. Actuator Driver Subsystem

Actuators inherit from the base `Actuator` class. The state machine resolves input triggers and physical outputs:

* **`ActuatorControlType`**:
  - `GPIO_OUTPUT`: Standard high/low relay controls.
  - `GPIO_PWM`: Pulse-width modulation outputs (used for dimmers).
* **Hold-to-Dim Logic (`LIGHT_DIMMER`)**:
  - Utilizes a non-blocking timer in `Actuator::loop()`.
  - Captures continuous button presses on input pins. Toggles dimming direction (increasing/decreasing brightness) when held, and saves the target brightness in configuration.
* **Shutter Calibration**: Covers/roller shutters utilize timed calibrations to map percentage states ($0-100\%$) to precise relay run times, preventing mechanical motor stress.

---

## 4. Sensor Driver Subsystem

Sensors inherit from the base `Sensor` class. Each sensor executes an independent polling loop:

* **Polling Timer**: `Sensor::loop()` runs periodically depending on the configured `delayRead` parameter.
* **Environmental Drivers**: Support for OneWire DS18B20 probes, DHT sensors, and I2C SHT4x sensors.
* **mmWave Presence Radars (HLK-LD2410/50/60)**:
  - Connect via Hardware/Software Serial.
  - Parse UART frames containing target distance, motion energy, and presence status, publishing updates immediately over MQTT.
  - **Multi-Target Tracking (LD2450/LD2460)**: Parses 2D target positions ($X$, $Y$) and velocities for up to 3/5 concurrent targets, registering individual coordinates as Home Assistant sensor entities dynamically.

---

## 5. HAN Portugal Smart Meter Integration

The HAN module turns the device into a Modbus Master that queries electricity meters (Kaifa, Landis+Gyr, Sagemcom) through a serial RS485 transceiver:

* **Modbus Protocol**: Uses `ModbusMaster` to send read requests for grid telemetry registers (Voltage, Current, Active Power, Power Factor, Tariff meters).
* **Scheduler**: Queries the meter every second and parses the response frames into structured grid parameters.
* **Home Assistant Mapping**: Automatically registers sensors for grid parameters, active power, and energy consumption.

---

## 6. How to Add a New Custom Feature/Driver

To add a new custom sensor or actuator driver to the firmware, follow these steps:

### Step 1: Define Driver Code
In [include/Constants.h](file:///c:/Users/bruno/CLionProjects/EasyIot/include/Constants.h), add a unique ID for your driver:
- Actuators should be added to `ActuatorDriver` (values `< 60`).
- Sensors should be added to `SensorDriver` (values $\ge 60$).

### Step 2: Implement Driver Logic
* If it is a sensor, implement the initialization in `Sensor::select()` and the reading logic in `Sensor::loop()` in `src/Sensors.cpp`.
* If it is an actuator, implement the output trigger logic in `Actuator::changeState()` and the physical GPIO write inside `Actuator::writeState()` in `src/Actuatores.cpp`.

### Step 3: Register Web Routing
Update `prepareNewFeature()` in `src/Templates.cpp` to map your new driver ID to your C++ class instantiator.
- Actuators will map through `prepareVirtualSwitch()`.
- Sensors will map through the switch-case statement inside `prepareNewFeature()`.

### Step 4: Add Home Assistant Discovery
Modify `HomeAssistantMqttDiscovery.cpp` to define the Home Assistant MQTT Auto-Discovery configuration payload for your new entity type.
