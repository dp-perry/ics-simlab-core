from devices.base import BaseDevice
import asyncio

class Tank(BaseDevice):
    async def run(self):
        """ Simulates a water tank filling up over time """
        while True:
            level = self.context.getValues(3, 0)[0] # Holding register 0
            new_level = (level + 1) % 100
            self.context.setValues(3, 0, [new_level])
            await asyncio.sleep(1)