import asyncio
import logging
import sys
from collections.abc import Callable
from types import SimpleNamespace
from typing import Any

from pymodbus import __version__ as pymodbus_version
from pymodbus.datastore import (
    ModbusSequentialDataBlock,
    ModbusServerContext,
    ModbusSlaveContext,
    ModbusSparseDataBlock,
)

from pymodbus.device import ModbusDeviceIdentification
from pymodbus.server import StartAsyncTcpServer

from facilities.bottling import create_bottling_facility

_logger = logging.getLogger(__file__)
_logger.setLevel(logging.INFO)

# Add a console handler if none exist
if not _logger.handlers:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    console_handler.setFormatter(formatter)
    _logger.addHandler(console_handler)

identity = ModbusDeviceIdentification

async def setup_server(comm, host, port, description=None, store="sequential", slaves=0, context=None, cmdline=None):
    """Run server setup"""
    args = SimpleNamespace()
    args.comm = comm
    args.host = host
    args.port = port
    args.description = description
    args.store = store
    args.slaves = slaves
    if context:
        args.context = context
    else:
        datablock: Callable[[], Any]
        _logger.info("### Create datastore")
        # The datastores only respond to the addresses that are initialized
        # If you initialize a DataBlock to addresses of 0x00 to 0xFF, a request to
        # 0x100 will respond with an invalid address exception
        # This is because many devices exhibit this kind of behavior (but not all)
        if args.store == "sequential": # The default
            # Continuing, use a sequential block without gaps.
            datablock = lambda : ModbusSequentialDataBlock(0x00, [17] * 100)  # pylint: disable=unnecessary-lambda-assignment
        elif args.store == "sparse":
            # Continuing, or use a sparse DataBlock which can have gaps
            datablock = lambda : ModbusSparseDataBlock({0x00: 0, 0x05: 1})  # pylint: disable=unnecessary-lambda-assignment
        elif args.store == "factory":
            # Alternately, use the factory methods to initialize the DataBlocks
            # or simply do not pass them to have them initialized to 0x00 on the
            # full address range::
            datablock = lambda : ModbusSequentialDataBlock.create()  # pylint: disable=unnecessary-lambda-assignment,unnecessary-lambda

        if args.slaves > 1:
            # The server then makes use of a server context that allows the server
            # to respond with different slave contexts for different slave ids.
            # By default, it will return the same context for every slave id supplied
            # (broadcast mode).
            # However, this can be overloaded by setting the single flag to False and
            # then supplying a dictionary of slave id to context mapping::
            context = {}

            for slave in range(args.slaves):
                context[slave] = ModbusSlaveContext(
                    di=datablock(),
                    co=datablock(),
                    hr=datablock(),
                    ir=datablock(),
                )

            single = False
        else:
            # The default
            context = ModbusSlaveContext(
                di=datablock(), co=datablock(), hr=datablock(), ir=datablock()
            )
            single = True

        # Build data storage
        args.context = ModbusServerContext(slaves=context, single=single)

    # set defaults
    comm_defaults: dict[str, list[int | str]] = {
        "tcp": ["socket", 5020],
        "udp": ["socket", 5020],
        "serial": ["rtu", "/dev/ptyp0"],
        "tls": ["tls", 5020],
    }
    args.framer = comm_defaults[comm][0]

    args.identity = ModbusDeviceIdentification(
        info_name={
            "VendorName": "SimICS",
            "ProductCode": "PM",
            "VendorUrl": "https://github.com/pymodbus-dev/pymodbus/",
            "ProductName": "SimICS Server",
            "ModelName": "SimICS 20250.7",
            "MajorMinorRevision": pymodbus_version,
        }
    )
    return args

async def run_async_server(args) -> None:
    """Run server"""
    txt = f"### start ASYNC server, listening on {args.port} - {args.comm}"
    _logger.info(txt)
    if args.comm == "tcp":
        address = (args.host, args.port)
        await StartAsyncTcpServer(
            context=args.context,
            identity=args.identity,
            address=address,
            # custom_functions=[], # allow custom handling
            framer=args.framer,
            # ignore_missing_slaves=True, # ignore request to a missing slave
            # broadcast_enable=False, # treat slave 0 as broadcast address,
            # timeout=1, # waiting time for request to complete
        )
    elif args.comm == "udp":
        pass
    elif args.comm == "serial":
        pass
    elif args.comm == "tls":
        pass


async def main():
    _logger.info("Creating bottling facility...")
    context, devices = create_bottling_facility()

    _logger.info("Setting up Modbus server...")
    run_args = await setup_server(
        comm='tcp',
        host='127.0.0.1',
        port=5020,
        description="Run asynchronous simulation",
        context=context,
        store="sequential", # "sequential", "sparse", "factory"
    )

    _logger.info("Starting simulation...")
    server_task = run_async_server(run_args)
    device_tasks = [device.run() for device in devices]

    await asyncio.gather(server_task, *device_tasks)

    # context, devices = create_bottling_facility()
    # tasks = [device.run() for device in devices]
    # server_task = StartTcpServer(context, address=("localhost", 5020), defer_start=True)
    #
    # await asyncio.gather(server_task.serve_forever(), *tasks)

if __name__ == "__main__":
    asyncio.run(main(), debug=True)