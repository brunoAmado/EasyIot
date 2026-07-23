# OnOfre Firmware Smoke Testing Guide

This guide describes the manual validation check list to run before certifying any release of the EasyIot firmware. It verifies that core features (Boot, Wi-Fi connectivity, MQTT discovery, and OTA upgrades) function correctly.

---

## 1. Boot Verification (Diagnostics)
1. Flash the target binary via USB-to-UART.
2. Connect a serial monitor (Baud: `115200`).
3. Reset/boot the device and check the serial output logs:
   * **Banner Check:** Ensure the bhonofre banner and startup logs appear.
   * **Version Verification:** Check that the printed version matches the compilation target (e.g. `9.17-dev`).
   * **Build Date:** Check that `buildDate:` matches the compilation timestamp.
   * **Relay Init:** Verify the relays initialize without boot-loop triggers.

---

## 2. Wi-Fi Connectivity
### AP Mode Fallback (First Boot / Reset)
1. Erase flash and boot the device.
2. Search for the captive portal AP (e.g., `OnOfre-XXXXXX`).
3. Connect and navigate to `http://192.168.4.1`.
4. Scan networks, select your router SSID, input the password, and click **Guardar**.
5. Verify that the browser performs a `POST` submit and redirects securely without leaking credentials in the URL.

### Station Mode
1. Verify the device disconnects AP mode and connects successfully to your Wi-Fi router.
2. Check that the device obtains an IP address and logs:
   ```text
   [SYSTEM] Connected, IP: 192.168.x.x
   ```

---

## 3. MQTT & Home Assistant Discovery
1. Verify the device establishes a connection to the MQTT broker (local Mosquitto or CloudIO).
2. Check the MQTT logs for discovery registry triggers:
   * **HA Discovery payload:** Ensure the JSON discovery topics are posted under `homeassistant/binary_sensor/.../config` or `homeassistant/switch/.../config`.
   * **State Updates:** Toggle a physical switch and check that the state payload (`ON` / `OFF`) is published correctly to the state topic.

---

## 4. OTA Firmware Upgrades
1. Open the local web panel of the device (`http://<ip-address>`).
2. Go to settings and trigger a local OTA upload using a newly compiled `.bin` file.
3. Verify that the upload completes successfully, the device restarts, reconnects to the network, and reports the updated version string.
