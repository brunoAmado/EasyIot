# Welcome to EasyIot Documentation

EasyIot is an open-source, lightweight, and highly customizable firmware for **ESP8266** and **ESP32** microcontrollers. It is designed to run locally, providing seamless integration with home automation hubs like **Home Assistant** without any external cloud dependencies.

---

## Key Features

* 🚀 **Captive Portal Setup**: Headless provisioning of local WiFi credentials, MQTT Broker IP, and custom features via a mobile-friendly web panel.
* 💡 **Dynamic Actuator & Sensor Engine**: Map switch inputs, relays, shutters, and presence radars (such as HLK-LD2410/50/60) to any free GPIO pins dynamically from the web panel.
* ⚡ **HAN Portugal Smart Meter Integration**: Native Modbus Master integration to query Kaifa, Landis+Gyr, or Sagemcom smart meters used by E-Redes, publishing real-time energy grid metrics.
* 🏡 **Home Assistant Auto-Discovery**: Automatic entity creation in Home Assistant over MQTT (no configuration.yaml changes required).
* 🛠️ **Non-Blocking Control**: Clean, state-driven C++ implementation utilizing asynchronous WebServers and MQTT clients for optimal responsiveness.

---

## Documentation Structure

* 🏁 **[Getting Started](How_To_Build_And_Configure.md)**: Setting up VS Code, PlatformIO compiler target overrides, provisioning workflows, and template selections.
* 🔌 **[Hardware Profiles](Hardware_Configuration_Profiles.md)**: Overview of preconfigured hardware boards (OnOfre boards, PZEM boards).
* 🎛️ **[Actuators & Relays](Actuator.md)**: How switches, relays, cover blind calibrations, and hold-to-dim dimmers work.
* 🌡️ **[Sensors & Radars](Sensor.md)**: Pin configuration and reading intervals for temperature, magnetic reeds, PIRs, and presence radars.
* 📖 **[Developer Reference](ConfigOnofre.md)**: In-depth structural overview of classes like `ConfigOnofre`, MQTT clients, and Modbus drivers.

---

## Quick-Start Checklist

1. **Build the Firmware**: Compile targets using VS Code + PlatformIO.
2. **Flash the Module**: Load the compiled `.bin` file via serial.
3. **Provision WiFi**: Connect to the Captive Portal access point `ONOFRE_xxxxxx` (Password: `bhonofre`) and navigate to `http://192.168.4.1` to select your home network.
4. **Link Home Assistant**: Enter your MQTT broker credentials. The device will automatically appear in Home Assistant!