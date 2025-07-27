from devices.bottling_plant import BottlingPlant
from pymodbus.datastore import ModbusServerContext, ModbusSlaveContext, ModbusSequentialDataBlock

def create_bottling_facility():
    slave_id = 1

    # Define a memory block with 16 holding registers
    datastore = ModbusSlaveContext(
        hr=ModbusSequentialDataBlock(0, [0]*16),
    )

    context = ModbusServerContext(slaves={slave_id: datastore}, single=False)

    devices = [
        BottlingPlant(context=context[1], unit_id=1)
    ]
    return context, devices