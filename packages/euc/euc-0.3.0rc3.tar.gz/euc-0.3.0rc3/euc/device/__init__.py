import pkg_resources


BLUEZ_DEVICE_INTF = "org.bluez.Device1"
UUIDS = "UUIDs"


class EUCError(Exception):
    pass


class DeviceDriverNotFound(EUCError):
    pass


class DeviceNotFound(EUCError):
    pass


def get_device_drivers():
    return (
        (entry_point.name, entry_point.load())
        for entry_point in pkg_resources.iter_entry_points("euc.device.driver")
    )


def prepare_device_obj(obj):
    return {k: v[1] for k, v in obj.items() if isinstance(v, tuple) and len(v) == 2}


async def get_devices(system_bus):
    bluez = system_bus["org.bluez"]
    itf = await bluez["/"].get_async_interface("org.freedesktop.DBus.ObjectManager")
    managed_objects = (await itf.GetManagedObjects())[0]
    return sorted(
        (
            (path, prepare_device_obj(obj[BLUEZ_DEVICE_INTF]))
            for (path, obj) in managed_objects.items()
            if BLUEZ_DEVICE_INTF in obj
        ),
        key=lambda item: item[1].get("RSSI", -1000),
        reverse=True,
    )


async def get_device(system_bus, device_path):
    devices = await get_devices(system_bus)
    for path, obj in devices:
        if path == device_path:
            return obj
    raise DeviceNotFound(device_path)


async def create_driver_instance(system_bus, driver_name, device_path):
    for name, driver_class in get_device_drivers():
        if driver_name == name:
            return driver_class.from_device(system_bus, device_path)
    raise DeviceDriverNotFound(driver_name)
