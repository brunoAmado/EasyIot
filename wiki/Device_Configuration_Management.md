# Device Configuration Management

> 30 nodes

## Key Concepts

- **ModbusMaster.cpp** (28 connections) — `src/ModbusMaster.cpp`
- **ModbusMasterTransaction** (12 connections) — `include/ModbusMaster.h`
- **ModbusMaster::begin()** (2 connections) — `src/ModbusMaster.cpp`
- **ModbusMaster::readCoils()** (2 connections) — `src/ModbusMaster.cpp`
- **ModbusMaster::readDiscreteInputs()** (2 connections) — `src/ModbusMaster.cpp`
- **ModbusMaster::readHoldingRegisters()** (2 connections) — `src/ModbusMaster.cpp`
- **ModbusMaster::readInputRegisters()** (2 connections) — `src/ModbusMaster.cpp`
- **ModbusMaster::readLastProfile()** (2 connections) — `src/ModbusMaster.cpp`
- **ModbusMaster::writeSingleCoil()** (2 connections) — `src/ModbusMaster.cpp`
- **ModbusMaster::writeSingleRegister()** (2 connections) — `src/ModbusMaster.cpp`
- **ModbusMaster::writeMultipleCoils()** (2 connections) — `src/ModbusMaster.cpp`
- **ModbusMaster::writeMultipleRegisters()** (2 connections) — `src/ModbusMaster.cpp`
- **ModbusMaster::maskWriteRegister()** (2 connections) — `src/ModbusMaster.cpp`
- **ModbusMaster::readWriteMultipleRegisters()** (2 connections) — `src/ModbusMaster.cpp`
- **crc16_update()** (2 connections) — `src/ModbusMaster.cpp`
- **ModbusMaster::ModbusMasterTransaction()** (2 connections) — `src/ModbusMaster.cpp`
- **ModbusMaster::ModbusMaster()** (1 connections) — `src/ModbusMaster.cpp`
- **Stream** (1 connections)
- **ModbusMaster::beginTransmission()** (1 connections) — `src/ModbusMaster.cpp`
- **ModbusMaster::requestFrom()** (1 connections) — `src/ModbusMaster.cpp`
- **ModbusMaster::sendBit()** (1 connections) — `src/ModbusMaster.cpp`
- **ModbusMaster::available()** (1 connections) — `src/ModbusMaster.cpp`
- **ModbusMaster::receive()** (1 connections) — `src/ModbusMaster.cpp`
- **ModbusMaster::idle()** (1 connections) — `src/ModbusMaster.cpp`
- **ModbusMaster::preTransmission()** (1 connections) — `src/ModbusMaster.cpp`
- *... and 5 more nodes in this community*

## Relationships

- [System Lifecycle & Network Provisioning](System_Lifecycle_&_Network_Provisioning.md) (1 shared connections)
- [MQTT Constants](MQTT_Constants.md) (1 shared connections)

## Source Files

- `include/ModbusMaster.h`
- `src/ModbusMaster.cpp`

## Audit Trail

- EXTRACTED: 60 (73%)
- INFERRED: 22 (27%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*