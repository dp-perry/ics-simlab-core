_This project is inspired by VirtuaPlant which is no longer being maintained._

Find the original VirtuaPlant here [https://github.com/jseidl/virtuaplant](https://github.com/jseidl/virtuaplant)


**-- This is currently a work in progress only the bottling facility works with no world view --** 

# ICS Simlab Core
ICS SimLab Core is a modular, Python-based simulation environment for industrial control systems (ICS) and SCADA networks. It emulates virtual facilities like bottling plants or oil processing units using Modbus TCP, allowing security researchers, students, and engineers to explore:

- Operational behavior of industrial processes
- Secure and insecure Modbus communications
- Real-world attack and defense scenarios
- HMI and automation testing using simulated sensors and actuators

The system uses a modern, asynchronous Python backend powered by [pymodbus](https://github.com/pymodbus-dev/pymodbus) == 3.9, and is designed to be extensible, readable, and realistic.

Find the world view here [https://github.com/dp-perry/ics-simlab-world](https://github.com/dp-perry/ics-simlab-world)

#### Further reading on the real world impacts of OT/ICS attacks**
In 2025, 600 apartment buildings in Ukraine lost heating for two days in sub-zero temperatures because of a malware abusing the Modbus protocol.
*" FrostyGoop sends Modbus commands to read or modify data on industrial control systems (ICS) devices, causing damage to the environment where attackers installed it"*
- https://unit42.paloaltonetworks.com/frostygoop-malware-analysis/
- https://www.dragos.com/blog/protect-against-frostygoop-ics-malware-targeting-operational-technology/

## Features
- Modbus TCP Server with multiple simulated devices
- State-based device simulation
- Live-updating registers representing sensors, actuators, and counters
- Inter-device logic emulates PLC-like behavior
- Easy to create new facilities
- Send register data to Worldview over websockets
- Receive sensor data from Worldview over websockets

## Requirements
- pymodbus v3.9.x - it looks like v4 is coming soon and will include breaking changes
- websocket if a worldview is used

## Virtual Enviroment
I personally prefer to use virtual environment for python projects. If you are unfamiliar with it, here is what you can do.
Documentation on virtual environments: [https://docs.python.org/3/library/venv.html](https://docs.python.org/3/library/venv.html)
```bash
# windows depending on your python install
py -m venv ics-env
# if the above does not work test with one of these below and use that option for all commands
python3 | python
# Again this one depends on your python install
# Activate the virutal enviroment, this will ensure that any installed packages only apply to this project.
source ics-env/bin/activate
```
And now continue with the commands below. Use ```deactivate``` to deactivate the virtual environment. After that, installs apply
globally again.

## Running a facility
Right now all scripts default to the bottling plant, the plant can be started by running
```bash
# Install packages
pip install -r requirements.txt

# Start plant
python3 main.py

# Optional
python3 ./worldview/server.py
```

Some example attack scripts are present in ./client.

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

## Future plans

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