import asyncio
import json
import websockets

from pymodbus.client import ModbusTcpClient

# Connect to local Modbus server (running in main.py)
client = ModbusTcpClient("127.0.0.1", port=5020)
is_busy = False

def read_reg(address):
    result = client.read_holding_registers(address, count=1)
    return result.registers[0] if result and not result.isError() else 0

def write_reg(address, value):
    print(f"Set {address}: {value}")
    client.write_register(address, value)

async def react_to_sensor():
    global is_busy
    is_busy = True
    print("🚰 Bottle detected - starting fill process")

    write_reg(4, 1)  # filler on
    await asyncio.sleep(10)
    write_reg(4, 0)  # filler off

    print("➡️ Filler done - starting conveyor")
    write_reg(2, 1)  # conveyor on
    await asyncio.sleep(10)
    write_reg(2, 0)  # conveyor off

    write_reg(1, 0)  # clear bottle sensor (optional)
    print("✅ Process complete")
    is_busy = False

async def websocket_handler(websocket):
    print("🔗 WebSocket client connected")
    try:
        while True:
            # Send current state to frontend
            state = {
                "conveyor_on": read_reg(2),
                "filler_on": read_reg(4),
                "bottle_present": read_reg(1),
                "water_level": read_reg(3),
                "power": read_reg(0),
                "bottle_count": read_reg(5),
            }
            await websocket.send(json.dumps(state))

            # Check if a message is waiting (non-blocking)
            try:
                message = await asyncio.wait_for(websocket.recv(), timeout=0.01)
                data = json.loads(message)
                register = data.get("register")
                value = data.get("value")
                if register is not None:
                    write_reg(register, value)
                    print(f"Updated register {register} with value {value}")

                    if register == 1 and value == 1 and not is_busy:
                        asyncio.create_task(react_to_sensor())
            except asyncio.TimeoutError:
                pass  # no message received during this frame

            await asyncio.sleep(0.25)

    except websockets.exceptions.ConnectionClosed:
        print("WebSocket client disconnected")

async def main():
    print("🌐 WebSocket server running on ws://localhost:8765")
    async with websockets.serve(websocket_handler, "0.0.0.0", 8765):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())