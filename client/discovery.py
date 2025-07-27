#!/usr/bin/env python3

# Read the values of the first 16 registers

import sys
import time
from pymodbus.client import ModbusTcpClient

if len(sys.argv) != 2:
    print("Error: Incorrect arguments given")
    print("Usage: ./discovery.py ip_address")
    sys.exit()

ip = sys.argv[1]

client = ModbusTcpClient(ip, port=5020)
client.connect()

while True:
    rr = client.read_holding_registers(1, count=16)
    print(rr.registers)
    time.sleep(1)
