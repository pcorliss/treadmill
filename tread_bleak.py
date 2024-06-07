import asyncio
from bleak import BleakScanner, BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic
import logging


TARGET_DEVICE_NAME = "LifeSpan"  # Replace with your device name or a part of it

INIT_SEQUENCE = [
    b"\x02\x00\x00\x00\x00",
    b"\xC2\x00\x00\x00\x00",
    b"\xE9\xFF\x00\x00\x00",
    b"\xE4\x00\xF4\x00\x00"
]

        # Start = 0xE1000000,
        # Stop = 0xE0000000,
        # GetSteps = 0xA1880000,
        # GetCalories = 0xA1870000,
        # GetDistance = 0xA1850000,
        # GetTime = 0xA1890000,
        # GetSpeed = 0xA1820000,

INFO_QUERIES = {
    "start":    b"\xE1\x00\x00\x00\x00",
    "stop":     b"\xE0\x00\x00\x00\x00",
    "unknown":  b"\xA1\x81\x00\x00\x00",
    "steps":    b"\xA1\x88\x00\x00\x00",
    "calories": b"\xA1\x87\x00\x00\x00",
    "distance": b"\xA1\x85\x00\x00\x00",
    "time":     b"\xA1\x89\x00\x00\x00",
    "speed":    b"\xA1\x82\x00\x00\x00"
}

logger = logging.getLogger(__name__)


async def discover_device():
    device = None
    while device is None:
        devices = await BleakScanner.discover()
        # map device names
        device_names = [device.name for device in devices]
        if TARGET_DEVICE_NAME in device_names:
            device = devices[device_names.index(TARGET_DEVICE_NAME)]
        else:
          print("Unable to find device. Retrying...")

    print(f"Found target device: {device.name} with address: {device.address}")
    return device.address

async def discover_characteristics(device_address):
  async with BleakClient(device_address) as client:
    services = await client.get_services()
    for service in services:
      print(f"Service: {service.uuid} ({service.handle})")
      print(f"  Description: {service.description}")
      for char in service.characteristics:
        # print all characteristic fields
        print(f"  Characteristic: {char.uuid} ({char.handle})")
        print(f"    Description: {char.description}")
        print(f"    Properties: {char.properties}")
        if 'read' in char.properties:
          val = await client.read_gatt_char(char.uuid)
          print(f"      Read: {val}")
        if 'write' in char.properties:
          print(f"      MaxWrite: {char.max_write_without_response_size}")

        for descriptor in char.descriptors:
          print(f"      Descriptor: {descriptor.uuid} ({descriptor.handle})")
          print(f"        Description: {descriptor.description}")

                    
async def main():
    device_address = await discover_device()
    if device_address:
        await discover_characteristics(device_address)
    else:
        print("Target device not found")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
