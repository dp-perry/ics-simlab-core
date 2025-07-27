import asyncio
import logging

_logger = logging.getLogger(__name__)

class BottlingPlant:
    def __init__(self, context, unit_id=1):
        self.context = context
        self.unit_id = unit_id

        # Register map
        self.REG_POWER = 0
        self.REG_BOTTLE_SENSOR = 1
        self.REG_CONVEYOR = 2
        self.REG_WATER_SENSOR = 3
        self.REG_FILLER = 4
        self.REG_BOTTLE_COUNT = 5

    def _read(self, reg):
        return self.context.getValues(3, reg, count=1)[0]

    def _write(self, reg, value):
        self.context.setValues(3, reg, [value])

    async def run(self):
        bottle_present = False

        while True:
            power = self._read(self.REG_POWER)
            if power == 0:
                self._write(self.REG_CONVEYOR, 0)
                self._write(self.REG_FILLER, 0)
                _logger.info("Facility off. Waiting...")
                await asyncio.sleep(1)
                continue

            bottle_sensor = self._read(self.REG_BOTTLE_SENSOR)
            water_sensor = self._read(self.REG_WATER_SENSOR)

            # Bottle detected and water level is OK → start filling
            if bottle_sensor and not water_sensor:
                self._write(self.REG_CONVEYOR, 0)
                self._write(self.REG_FILLER, 1)
                _logger.info("Filling bottle...")

                # Increment bottle counter if not already filling
                if not self._read(self.REG_FILLER):
                    count = self._read(self.REG_BOTTLE_COUNT)
                    self._write(self.REG_BOTTLE_COUNT, count + 1)
                    _logger.info(f"Total bottles filled: {count + 1}")

            # Bottle detected but water is full → stop filler, move bottle
            elif bottle_sensor and water_sensor:
                self._write(self.REG_FILLER, 0)
                self._write(self.REG_CONVEYOR, 1)
                _logger.info("Water full. Moving bottle...")

            # No bottle → run conveyor
            elif not bottle_sensor:
                self._write(self.REG_FILLER, 0)
                self._write(self.REG_CONVEYOR, 1)
                _logger.info("Waiting for next bottle...")

            # Simulate bottle passing every 5s
            bottle_present = not bottle_present
            self._write(self.REG_BOTTLE_SENSOR, int(bottle_present))

            await asyncio.sleep(2)