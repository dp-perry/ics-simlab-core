from abc import ABC, abstractmethod

class BaseDevice(ABC):
    def __init__(self, name, context, unit_id):
        self.name = name # Human-readable name of the device
        self.context = context # Modbus context for reading/writing registers
        self.unit_id = unit_id # Modbus Unit ID

    @abstractmethod
    async def run(self):
        """Simulate device behavior (to be run in an event loop)"""
        pass