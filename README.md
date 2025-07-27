_This project is inspired by VirtuaPlant which is no longer being maintained._

Find the original VirtuaPlant here [https://github.com/jseidl/virtuaplant](https://github.com/jseidl/virtuaplant)


**-- This is currently a work in progress only the bottling facility works with no world view --** 

# ICS Simlab Core
ICS SimLab Core is a modular, Python-based simulation environment for industrial control systems (ICS) and SCADA networks. It emulates virtual facilities like bottling plants or oil processing units using Modbus TCP, allowing security researchers, students, and engineers to explore:

- Operational behavior of industrial processes
- Secure and insecure Modbus communications
- Real-world attack and defense scenarios
- HMI and automation testing using simulated sensors and actuators

The system uses a modern, asynchronous Python backend powered by pymodbus == 3.9, and is designed to be extensible, readable, and realistic.

Find the world view here [https://github.com/dp-perry/ics-simlab-world](https://github.com/dp-perry/ics-simlab-world)

## Features
- Modbus TCP Server with multiple simulated devices
- State-based device simulation
- Live-updating registers representing sensors, actuators, and counters
- Inter-device logic emulates PLC-like behavior
- Easy to create new facilities

## Current facilities
### Bottling plant register
- 0: Master switch, turn facility on or off. Default: 0
- 1: Bottle sensor, is there a bottle under the filler?
- 2: Conveyor state, 1 = moving, 0 = stopped
- 3: Water level, 1 = bottle is full stops filling
- 4: Filler, 1 = filling, 0 is idle
- 5: Bottle Counter, tracks the number of bottles filled

### Oil Refinery Boiler
- WiP

## Future
In honor of VirtuaPlant this project will aim to create these future facilities and protocols.

### Future facilities
- Oil Refinery Boiler
- Nuclear Power Plant Reactor
- Steel Plant Furnace

## Future protocols
- DNP3 (based on OpenDNP3)
- S7

## Future features
- HMI to control plant devices through a UI interface
- Random faults
- Manager that will try to respond to potential cyberattacks (turn facility off, try to disconnect attacker)
- Specific scenario's to play through