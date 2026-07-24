# Hardware Access & Sensor Drivers

> 42 nodes

## Key Concepts

- **CloudIO.cpp** (16 connections) — `src/CloudIO.cpp`
- **mqttConnected()** (14 connections) — `src/Mqtt.cpp`
- **Actuator::notifyState()** (9 connections) — `src/Actuatores.cpp`
- **Mqtt.cpp** (9 connections) — `src/Mqtt.cpp`
- **reconnect()** (9 connections) — `src/Mqtt.cpp`
- **publishOnMqtt()** (9 connections) — `src/Mqtt.cpp`
- **wifiConnected()** (7 connections) — `src/CoreWiFi.cpp`
- **addToHomeAssistant()** (7 connections) — `src/HomeAssistantMqttDiscovery.cpp`
- **initHomeAssistantDiscovery()** (6 connections) — `src/HomeAssistantMqttDiscovery.cpp`
- **Sensor::notifyState()** (6 connections) — `src/Sensors.cpp`
- **sendToServerEvents()** (6 connections) — `src/WebServer.cpp`
- **HomeAssistantMqttDiscovery.cpp** (5 connections) — `src/HomeAssistantMqttDiscovery.cpp`
- **createHaSwitch()** (5 connections) — `src/HomeAssistantMqttDiscovery.cpp`
- **loopMqtt()** (5 connections) — `src/Mqtt.cpp`
- **notifyStateToCloudIO()** (4 connections) — `src/CloudIO.cpp`
- **connectToCloudIO()** (4 connections) — `src/CloudIO.cpp`
- **removeFromHomeAssistant()** (4 connections) — `src/HomeAssistantMqttDiscovery.cpp`
- **callbackMqtt()** (4 connections) — `src/Mqtt.cpp`
- **connectToCloudIOMqtt()** (3 connections) — `src/CloudIO.cpp`
- **subscribeOnMqttCloudIO()** (3 connections) — `src/CloudIO.cpp`
- **onMqttConnect()** (3 connections) — `src/CloudIO.cpp`
- **onMqttDisconnect()** (3 connections) — `src/CloudIO.cpp`
- **cloudIOConnected()** (3 connections) — `src/CloudIO.cpp`
- **setupMqttCloudIO()** (3 connections) — `src/CloudIO.cpp`
- **tryMqttCloudConnection()** (3 connections) — `src/CloudIO.cpp`
- *... and 17 more nodes in this community*

## Relationships

- [Modbus Protocol Master Driver](Modbus_Protocol_Master_Driver.md) (6 shared connections)
- [Web Panel Frontend & Templates](Web_Panel_Frontend_&_Templates.md) (5 shared connections)
- [Shutter Calibration & Math](Shutter_Calibration_&_Math.md) (3 shared connections)
- [Profile Template Declarations](Profile_Template_Declarations.md) (2 shared connections)
- [CloudIO & MQTT Declarations](CloudIO_&_MQTT_Declarations.md) (1 shared connections)
- [Captive Portal Header](Captive_Portal_Header.md) (1 shared connections)
- [MQTT Client & HA Discovery](MQTT_Client_&_HA_Discovery.md) (1 shared connections)

## Source Files

- `src/Actuatores.cpp`
- `src/CloudIO.cpp`
- `src/ConfigOnofre.cpp`
- `src/CoreWiFi.cpp`
- `src/HomeAssistantMqttDiscovery.cpp`
- `src/Mqtt.cpp`
- `src/Sensors.cpp`
- `src/WebServer.cpp`

## Audit Trail

- EXTRACTED: 117 (65%)
- INFERRED: 62 (35%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*