# Firmware Rollback & Recovery Guide

If a firmware release or OTA update fails, crashes the device, or results in a boot loop, follow this guide to restore the device to a functional state.

---

## 1. Triggering Flash Mode (UART Bootloader)
If the device is unresponsive or in a boot loop, you must flash it over serial:
1. Connect a USB-to-UART adapter (3.3V levels only!) to the device's TX, RX, and GND pins.
2. Hold the **GPIO0 (Boot)** pin/button down.
3. Power cycle or reset the device (pull **RST** low and release).
4. Release the GPIO0 pin. The MCU is now in UART programming mode.
5. Run the PlatformIO upload command:
   ```bash
   pio run -e <env-name> --target upload
   ```

---

## 2. Hard Resetting Flash (Erasing Corrupted Configurations)
If a configuration gets corrupted in NVS (ESP32) or LittleFS (ESP8266), the device might crash on boot. You must completely wipe the flash memory:

### Using esptool (Recommended)
1. Install esptool:
   ```bash
   pip install esptool
   ```
2. Put the device in flash mode (see Section 1).
3. Erase the entire flash chip:
   * **ESP8266:**
     ```bash
     esptool.py --port <COM-PORT> erase_flash
     ```
   * **ESP32:**
     ```bash
     esptool.py --chip esp32 --port <COM-PORT> erase_flash
     ```
4. Re-flash the firmware via PlatformIO. This will rebuild a fresh partition table and format the filesystem.

---

## 3. Local Version Rollbacks
Always maintain backups of stable release binaries. If a newly deployed version is unstable:
1. Fetch the binary of the previous stable release.
2. If the local web panel is still accessible, navigate to `http://<device-ip>/update` and upload the stable binary.
3. If the web panel is inaccessible, flash the stable binary over serial using `esptool.py`:
   ```bash
   esptool.py --port <COM-PORT> --baud 460800 write_flash 0x0 <stable-firmware>.bin
   ```
