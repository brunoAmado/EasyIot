# Web Interface Control & Configuration Guide

The BH-OnOfre local web interface allows you to monitor telemetry, control actuators, and configure network, MQTT, and virtual hardware mappings.

---

## 1. Header Dashboard (Live Status)

At the top of the interface, the header dashboard displays live telemetry:
* **Wi-Fi Signal**: Shows the active Wi-Fi SSID and real-time signal strength percentage.
* **Device Name (`nodeId`)**: Allows you to rename the device (e.g., `living-room`). Shows the hardware Chip ID next to it.
* **MQTT Status**: A color-coded LED indicator showing MQTT broker connectivity (Green: Connected, Red/Grey: Disconnected).
* **Guardar (Save)**: Clicking this button commits all pending settings to the device's flash storage.

---

## 2. System Tab (SISTEMA)

This section controls the underlying network, credentials, and system utilities:

### A. Access Credentials
* **AP Password**: Change the fallback Wi-Fi Hotspot password (defaults to `bhonofre`).
* **Admin Login**: Set a username (`apiUser`) and password (`apiPassword`) to secure access to the local web panel.

### B. Network Settings (Wi-Fi)
* **SSID & Password**: Enter the Wi-Fi credentials of your home network.
* **DHCP Toggle**: Enable DHCP for automatic IP configuration, or disable it to configure a static IP, Gateway, and Netmask.

### C. MQTT Settings
* **Broker IP / DNS**: The address of your Home Assistant Mosquitto broker (or OnofreCloud).
* **Port & Credentials**: Default port `1883`, with optional username and password.

### D. System Tools & Backups
* **Reset**: Wipes the LittleFS partition and restores factory settings.
* **Backup**: Downloads the entire configuration (Wi-Fi, MQTT, registered features) as a JSON backup file.
* **Restaurar (Restore)**: Uploads a backup JSON file to restore settings.
* **Reiniciar (Reboot)**: Safely restarts the microcontroller.
* **Local OTA Installer**: Allows you to select and upload a compiled `firmware.bin` file to upgrade the firmware over-the-air.

---

## 3. Functions Tab (FUNÇÕES)

This is the main control dashboard where active features are displayed, edited, and added:

### A. Controlling Actuators & Viewing Telemetry
* **Switches & Lights**: Toggle on/off directly from the dashboard.
* **Dimmer Slider**: drag the horizontal range slider ($0-100\%$) to adjust brightness level.
* **Roller Shutter Slider**: drag the slider ($0-100\%$) to position covers/blinds.
* **HAN Portugal Smart Meter Widget**:
  - Live Imported vs Exported power (in Watts).
  - Contracted power (kVA) and active Tariff rate indicator (Vazio, Ponta, Cheias).
  - Expanded diagnostics showing grid Voltage, Current, Frequency, Power Factor, and accumulated imported/exported active/reactive energy meters.

### B. Virtual Feature Editor (Clicking `...` on a widget)
Each widget has an editing menu where you can:
* **Rename**: Customize the display name.
* **Input Mode**: Select **Pulsador** (momentary wall push-button) or **Normal** (standard on/off toggle wall switch).
* **Calibration**: Set the exact time in seconds for **shutter opening (Subir)** and **closing (Descer)** to ensure precise blind level mapping.
* **Auto-Off**: Set a timeout in seconds to automatically toggle the relay OFF after activation (useful for garden valves or security pulses).
* **KNX Group binding**: Set area, line, and member numbers to bind this actuator directly to your local KNX physical group address.
* **Eliminar (Delete)**: Remove the feature from the device configuration.

### C. Adding a New Feature (Add Button `+`)
Click the `+` button to open the Feature Wizard:
1. **Name**: Define a name for the new feature.
2. **Driver**: Choose from 18+ native hardware drivers (e.g. Switch, Cover, Dimmer, Garage door, DHT11/22 temperature probe, DS18B20 temperature, reed door sensor, motion PIR, HLK-LD2410 mmWave presence radar, or PZEM-004T energy monitor).
3. **GPIO Pin Mapping**: Select physical input and output GPIO pins from dropdown lists containing only safe, validated pins for your board model.
