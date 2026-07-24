# System Lifecycle & Network Provisioning

> 56 nodes

## Key Concepts

- **ModbusMaster** (64 connections) — `include/ModbusMaster.h`
- **idle** (1 connections) — `include/ModbusMaster.h`
- **preTransmission** (1 connections) — `include/ModbusMaster.h`
- **postTransmission** (1 connections) — `include/ModbusMaster.h`
- **ku8MBIllegalFunction** (1 connections) — `include/ModbusMaster.h`
- **ku8MBIllegalDataAddress** (1 connections) — `include/ModbusMaster.h`
- **ku8MBIllegalDataValue** (1 connections) — `include/ModbusMaster.h`
- **ku8MBSlaveDeviceFailure** (1 connections) — `include/ModbusMaster.h`
- **ku8MBSuccess** (1 connections) — `include/ModbusMaster.h`
- **ku8MBInvalidSlaveID** (1 connections) — `include/ModbusMaster.h`
- **ku8MBInvalidFunction** (1 connections) — `include/ModbusMaster.h`
- **ku8MBResponseTimedOut** (1 connections) — `include/ModbusMaster.h`
- **ku8MBInvalidCRC** (1 connections) — `include/ModbusMaster.h`
- **setTransmitBuffer** (1 connections) — `include/ModbusMaster.h`
- **clearTransmitBuffer** (1 connections) — `include/ModbusMaster.h`
- **beginTransmission** (1 connections) — `include/ModbusMaster.h`
- **requestFrom** (1 connections) — `include/ModbusMaster.h`
- **sendBit** (1 connections) — `include/ModbusMaster.h`
- **receive** (1 connections) — `include/ModbusMaster.h`
- **readCoils** (1 connections) — `include/ModbusMaster.h`
- **readDiscreteInputs** (1 connections) — `include/ModbusMaster.h`
- **readHoldingRegisters** (1 connections) — `include/ModbusMaster.h`
- **writeSingleCoil** (1 connections) — `include/ModbusMaster.h`
- **writeSingleRegister** (1 connections) — `include/ModbusMaster.h`
- **writeMultipleCoils** (1 connections) — `include/ModbusMaster.h`
- *... and 31 more nodes in this community*

## Relationships

- [Captive Portal Header](Captive_Portal_Header.md) (6 shared connections)
- [MQTT Constants](MQTT_Constants.md) (2 shared connections)
- [Device Configuration Management](Device_Configuration_Management.md) (1 shared connections)

## Source Files

- `include/ModbusMaster.h`

## Audit Trail

- EXTRACTED: 119 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*