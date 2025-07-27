import sys
import time
from pymodbus.client import ModbusTcpClient

if len(sys.argv) != 2:
    print("Error: Incorrect arguments given")
    print("Usage: ./discovery.py ip_address")
    sys.exit()

ip = sys.argv[1]

def read_register(address, register):
    client = ModbusTcpClient(ip, port=5020)
    client.connect()

    while True:
        rr = client.read_holding_registers(0, count=16)
        print(rr.registers)
        time.sleep(1)



if __name__ == "__main__":
    read_register(1, 1)