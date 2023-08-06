import logging
import ravel
import asyncio
import euc.device
import argparse


async def list_devices(system_bus):
    print("{0:30s} {1:>4} {2}".format("Name", "RSSI", "Path"))
    for path, device in await euc.device.get_devices(system_bus):
        rssi = device.get("RSSI", "")
        name = device.get("Name", "unknown")
        print(f"{name:30s} {rssi:>4} {path}")
    return


async def connect(system_bus, driver_name, device_path):
    device_driver = await euc.device.create_driver_instance(
        system_bus, driver_name, device_path
    )
    device_driver.add_properties_changed_callback(
        lambda self, props: print(f"{self.properties!r}")
    )
    await device_driver.run()


def list_drivers():
    print("\n".join(name for name, _ in euc.device.get_device_drivers()))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="action")
    list_devices_action = subparsers.add_parser("list_devices")
    list_drivers_action = subparsers.add_parser("list_drivers")
    connect_action = subparsers.add_parser("connect")
    connect_action.add_argument("driver_name")
    connect_action.add_argument("device_path")

    opts = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)
    system_bus = ravel.system_bus()
    loop = asyncio.get_event_loop()
    system_bus.attach_asyncio(loop)

    if opts.action == "list_devices":
        loop.run_until_complete(list_devices(system_bus))
    elif opts.action == "list_drivers":
        list_drivers()
    elif opts.action == "connect":
        loop.run_until_complete(connect(system_bus, opts.driver_name, opts.device_path))
