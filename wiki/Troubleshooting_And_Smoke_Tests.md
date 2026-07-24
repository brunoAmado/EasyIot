# Troubleshooting, Smoke Testing, & Recovery Guide

This guide outlines how to verify the firmware integrity, run diagnostic checkups, and recover from boot loops or failed updates.

---

## 1. Release Smoke Testing (Verification Checklist)

Run these checks to certify that a newly built firmware binary is stable before deploying it to production devices:

### A. Boot & Diagnostics Check
1. Flash the target binary to your test board via serial.
2. Connect a Serial Monitor with baud rate **`115200`** and reboot the device.
3. Verify that the startup log prints:
   - The EasyIot logo banner.
   - The correct firmware version (e.g. `9.17-dev`) and compilation build date.
   - Boot diagnostics (confirming LittleFS mounts successfully and relays initialize without power triggers).

### B. Wi-Fi & Captive Portal Test
1. Disconnect the device from your home network (or boot it with no saved Wi-Fi details).
2. Scan for the fallback Access Point (e.g., `ONOFRE_xxxxxx`).
3. Connect using password **`bhonofre`**, open your browser to `http://192.168.4.1`, and save your Wi-Fi settings.
4. Verify that:
   - Credentials are submitted securely via `POST` (no password in the URL).
   - The device reconnects successfully to your router and shuts down the AP.

### C. MQTT & Auto-Discovery Check
1. Monitor your MQTT broker (e.g., via `mosquitto_sub` or Home Assistant log outputs).
2. Confirm that the device registers itself and publishes JSON discovery payloads under `homeassistant/binary_sensor/.../config` or `homeassistant/switch/.../config`.
3. Toggle a physical switch and verify that state changes are published instantly.

---

## 2. Firmware Recovery & Rollback Procedures

If a device becomes unresponsive, boots into a loop, or experiences configuration corruption, follow these steps to recover:

### A. Entering Serial Flash Mode (UART Bootloader)
To recover an unresponsive board over serial:
1. Connect a USB-to-UART serial adapter (set to **`3.3V`** levels!) to the device's **TX**, **RX**, and **GND** pins.
2. Hold down the **GPIO0 (Flash/Boot)** button.
3. Power cycle the board (or pull **RST** low and release).
4. Release the GPIO0 button. The MCU is now in UART bootloader mode and ready to accept binaries.
5. In VS Code / PlatformIO, run the upload task:
   ```bash
   pio run -t upload -e <environment-name>
   ```

### B. Full Flash Chip Wipe (Fixing NVS / LittleFS Corruption)
If a filesystem or non-volatile storage block gets corrupted (causing the board to crash on boot), you must completely format the flash:
1. Install **`esptool`** on your computer:
   ```bash
   pip install esptool
   ```
2. Put the device in UART Bootloader Mode (see above).
3. Wipe the entire flash memory:
   - **ESP8266:**
     ```bash
     esptool.py --port <COM-PORT> erase_flash
     ```
   - **ESP32:**
     ```bash
     esptool.py --chip esp32 --port <COM-PORT> erase_flash
     ```
4. Re-flash the firmware binary using PlatformIO. This will rebuild clean partition tables and format a fresh LittleFS drive.

### C. Web UI OTA Rollback
If the device is still booting and connected to Wi-Fi but running an unstable firmware version, you can roll back using the local Web Page:
1. Compile or download the previous stable `.bin` file.
2. Navigate to `http://<device-ip-address>/update` in your browser.
3. Select the stable `.bin` file and upload it. The device will automatically flash, reboot, and reconnect.
