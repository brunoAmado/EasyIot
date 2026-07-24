# EasyIot User Guide

This guide helps end-users configure and use their EasyIot-flashed smart home devices.

---

## 1. Network & WiFi Provisioning

When the device boots for the first time, or if the saved WiFi credentials are no longer reachable, it automatically enters **Access Point (AP)** mode to allow configuration:

1. Connect to the WiFi network named `ONOFRE_xxxxxx` (where `xxxxxx` is a unique device ID).
2. Enter the default password: **`bhonofre`**
3. Open your browser and navigate to `http://192.168.4.1` (or `http://onofre.local`).
4. Under the WiFi tab:
   - **WiFi Scan:** Select your home network SSID from the list of scanned networks.
   - **Password:** Enter your home WiFi password.
   - **DHCP / Static IP:** Keep DHCP enabled for automatic IP assignment, or disable it to configure a static IP, Netmask, and Gateway.
5. Click **Save**. The device will reboot and connect to your home WiFi.

---

## 2. MQTT Broker Configuration

EasyIot uses MQTT for local communication. To connect the device to your MQTT broker (such as Mosquitto inside Home Assistant):

1. Access the web panel by entering the device's IP address (visible on your router) or navigating to `http://<nodeId>.local`.
2. Under the **MQTT Settings** tab, configure:
   - **MQTT Server:** The IP address of your broker.
   - **Port:** Default is `1883`.
   - **User / Password:** Your broker credentials (if authentication is enabled).
   - **Node ID:** A unique name for this device (e.g. `living-room-lights`). This determines the root of your MQTT topics (e.g. `onofre/living-room-lights/...`).
3. Click **Save**. Once connected, the device status LED will indicate a stable connection.

---

## 3. Home Assistant Integration

EasyIot fully supports **Home Assistant Auto-Discovery** via MQTT:

* Once the device connects to the broker, it automatically publishes configuration payloads to `homeassistant/light/.../config`, `homeassistant/switch/.../config`, etc.
* Home Assistant will instantly detect the device. You can find it under **Settings -> Devices & Services -> MQTT**.
* You do **not** need to manually add anything to your `configuration.yaml`!

---

## 4. Hardware Controls & Features

### A. Predefined Hardware Profiles (Templates)
EasyIot comes with preconfigured GPIO layouts for standard hardware. Go to **Settings -> Templates** and select:
* **Dual Light / Switch**: Configures two relays and two wall push-button inputs.
* **Cover (Blinds)**: Configures two relays (Up/Down) with interlock safety protection and inputs.
* **Garage Gate**: Configures a gate motor relay, toggle switches, and open/close magnetic reed status sensors.
* **HAN Module**: Configures a serial Modbus port to read real-time grid metrics from smart energy meters (Kaifa, Landis+Gyr, Sagemcom).
* **Garden Valves**: Configures multi-channel relay irrigation valves with built-in timeouts.

### B. Dynamic Custom Features (New Features)
If you have a custom DIY board, you can add features dynamically via the web panel by specifying:
- **Actuators (driverCode < 60)**: Add custom lights, toggle switches, or dimmers, selecting the exact output and input GPIO pins.
- **Sensors (driverCode >= 60)**: Add custom sensors:
  - **Reeds / Switches**: Door and window state sensors.
  - **Environmental**: DHT11/21/22 or DS18B20 temperature/humidity probes.
  - **Presence Radars**: HLK-LD2410, LD2450, or LD2460 mmWave radar presence sensors. For 2D tracking radars (like LD2450 and LD2460), individual target coordinates (X, Y position, and speed for up to 3/5 targets) are automatically exposed as numeric sensors in Home Assistant, enabling advanced automation based on zones and real-time positioning minimaps.
  - **Power Monitors**: PZEM-004T energy monitors.

---

## 5. Device Maintenance & OTA Updates

* **Web UI Control**: Toggle relays, view sensor parameters, and check connection details directly on the web dashboard.
* **OTA Firmware Update**: Update the firmware over-the-air. Go to the web panel's **Update** page and upload the compiled `firmware.bin` file, or trigger an auto-update from the configured CloudIO backend.
