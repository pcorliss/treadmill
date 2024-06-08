import asyncio
from bleak import BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic
import os

DEVICE_ADDRESS = '968C8C0A-BFD0-EBCD-E5E0-A0CB16F0BFE9'  # Replace with your device's address
# Characteristic: 0000fff1-0000-1000-8000-00805f9b34fb (81)
CHARACTERISTIC_UUID = '0000fff1-0000-1000-8000-00805f9b34fb' # Solid Blue - None
# Characteristic: 0000fff2-0000-1000-8000-00805f9b34fb (84)
# CHARACTERISTIC_UUID = '0000fff2-0000-1000-8000-00805f9b34fb' # Solid Blue - None
# Characteristic: 49535343-4c8a-39b3-2f49-511cff073b7e (86)
# CHARACTERISTIC_UUID = '49535343-4c8a-39b3-2f49-511cff073b7e' # None
# Characteristic: 49535343-026e-3a9b-954c-97daef17e26e (49)
# CHARACTERISTIC_UUID = '49535343-026e-3a9b-954c-97daef17e26e' # None
# Characteristic: 49535343-aca3-481c-91ec-d85e28a60318 (65)
# CHARACTERISTIC_UUID = '49535343-aca3-481c-91ec-d85e28a60318'

INIT_SEQUENCE = [
    b"\x02\x00\x00\x00\x00",
    b"\xC2\x00\x00\x00\x00",
    b"\xE9\xFF\x00\x00\x00",
    b"\xE4\x00\xF4\x00\x00"
]

CMDS = {
    "start":    b"\xE1\x00\x00\x00\x00",
    "stop":     b"\xE0\x00\x00\x00\x00",
}

#   def speed=(new_speed)
#     new_speed = (new_speed * 100.0).round
#     units = new_speed / 100
#     hundredths = new_speed % 100
#     send_command([0xd0, units, hundredths,0, 0].pack('C*'))
#   end

INFO_QUERIES = {
    # "steps":    b"\xA1\x88\x00\x00\x00",
    # "calories": b"\xA1\x87\x00\x00\x00",
    "distance": b"\xA1\x85\x00\x00\x00",
    "time":     b"\xA1\x89\x00\x00\x00",
    "speed":    b"\xA1\x82\x00\x00\x00"
}

def handle_rx(_: BleakGATTCharacteristic, data: bytearray):
    print("received:", data)
    print("alt: ", list(data[2:5]))

async def run(address):
    async with BleakClient(address) as client:
        # Write INIT_SEQUENCE
        for command in INIT_SEQUENCE:
            await client.write_gatt_char(CHARACTERISTIC_UUID, command)

        await client.start_notify(CHARACTERISTIC_UUID, handle_rx)


        # Query information
        for name, query in INFO_QUERIES.items():
            print("sending:", name)
            await client.write_gatt_char(CHARACTERISTIC_UUID, query, response=False)
            await asyncio.sleep(3)
            # response = await client.read_gatt_char(CHARACTERISTIC_UUID)
            # print(f"{name}: {response}")
            # response = await client.read_gatt_descriptor(86)
            # print(f"{name}: {response}")

        # Works!!!
        # # Start the device
        # await client.write_gatt_char(CHARACTERISTIC_UUID, CMDS["start"])
        # await asyncio.sleep(10)
        # # Stop the device
        # await client.write_gatt_char(CHARACTERISTIC_UUID, CMDS["stop"])


loop = asyncio.get_event_loop()
loop.run_until_complete(run(DEVICE_ADDRESS))
