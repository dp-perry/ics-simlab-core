#!/usr/bin/env python3

# Sets a single register to a value once

import sys
from pymodbus.client import ModbusTcpClient

if len(sys.argv) != 4:
    print("Error: Incorrect arguments given, expects 3")
    print("Usage: ./discovery.py ip_address registry value")
    sys.exit()

# Set values
ip = sys.argv[1]
registry = int(sys.argv[2])
value = int(sys.argv[3])

# Connect to Modbus
client = ModbusTcpClient(ip, port=5020)
client.connect()
client.write_register(registry, value)

print(f'Wrote {value} to registry: {registry}')