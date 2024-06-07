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

EXCLUDE_CHARACTERISTICS = [
  '49535343-aca3-481c-91ec-d85e28a60318',
  '49535343-026e-3a9b-954c-97daef17e26e',
]

# This one creates a solid light after init
INCLUDE_CHARACTERISTICS = [
  '0000fff1-0000-1000-8000-00805f9b34fb',
]

async def discover_characteristics(device_address):
  async with BleakClient(device_address) as client:
    services = await client.get_services()
    for service in services:
      for char in service.characteristics:
        if "write" in char.properties:
          if char.uuid in INCLUDE_CHARACTERISTICS:
            print(f"Service: {service.uuid}")
            print(f"  Characteristic: {char.uuid}, Properties: {char.properties}")
            await init_sequence(client, char.uuid)
            print("  Init Compoleted")
            print(f"max_write_size: {char.max_write_without_response_size}")
            response = await client.write_gatt_char(char.uuid, INFO_QUERIES["stop"])
            print(f"Resp: {response}")


def notification_handler(characteristic: BleakGATTCharacteristic, data: bytearray):
    """Simple notification handler which prints the data received."""
    logger.info("%s: %r", characteristic.description, data)

                    
# if "read" in char.properties:
#     print(f"    -> This characteristic supports reading.")
#     data = await client.read_gatt_char(char.uuid)
#     print(f"    -> Value: {data}")

async def steps(client, characteristic_uuid):
  await client.write_gatt_char(characteristic_uuid, INFO_QUERIES["steps"])

async def init_sequence(client, characteristic_uuid):
  for command in INIT_SEQUENCE:
    await client.write_gatt_char(characteristic_uuid, command)

async def main():
    device_address = await discover_device()
    if device_address:
        await discover_characteristics(device_address)
    else:
        print("Target device not found")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
