import asyncio
from bleak import BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic
import queue

DEVICE_ADDRESS = '968C8C0A-BFD0-EBCD-E5E0-A0CB16F0BFE9'  # Replace with your device's address
CHARACTERISTIC_UUID = '0000fff1-0000-1000-8000-00805f9b34fb' # Solid Blue - None

INIT_SEQUENCE = [
    b"\x02\x00\x00\x00\x00",
    b"\xC2\x00\x00\x00\x00",
    b"\xE9\xFF\x00\x00\x00",
    b"\xE4\x00\xF4\x00\x00"
]

CMDS = {
    "start":    b"\xE1\x00\x00\x00\x00",
    "stop":     b"\xE0\x00\x00\x00\x00",
    "speed":    b"\xD0\x00\x00\x00\x00",
}

# Set speed 0.4 -> 3.0 MPH
def speed_cmd(speed):
    units = int(speed)
    hundredths = int(speed * 100) % 100
    return b"\xD0" + units.to_bytes(1, 'little') + hundredths.to_bytes(1, 'little') + b"\x00\x00"

INFO_QUERIES = {
    # "steps":    b"\xA1\x88\x00\x00\x00",
    # "calories": b"\xA1\x87\x00\x00\x00",
    "distance": b"\xA1\x85\x00\x00\x00",
    "time":     b"\xA1\x89\x00\x00\x00",
    "speed":    b"\xA1\x82\x00\x00\x00"
}

q = queue.Queue()

def handle_rx(_: BleakGATTCharacteristic, data: bytearray):
    data_name = q.get()
    if data_name == "speed":
        print("Speed:", decode_speed(data))
    elif data_name == "distance":
        print("Distance:", decode_distance(data))
    elif data_name == "time":
        t = decode_time(data)
        h, m, s = t
        print(f"Time: {h:d}:{m:02d}:{s:02d}")
    elif data_name == "init":
        pass
    else:
        print("received:", data_name, data, list(data))

# Speed in MPH
def decode_speed(data):
    return data[2] + (data[3] / 100)

# Distance in Miles
def decode_distance(data):
    return data[2] + (data[3] / 100)

# Time in HH:MM:SS
def decode_time(data):
    return list(data[2:5])

async def send_cmd(client, cmd, name):
    q.put(name)
    await client.write_gatt_char(CHARACTERISTIC_UUID, cmd, response=False)
    await asyncio.sleep(5)

async def run(address):
    async with BleakClient(address) as client:
        # Write INIT_SEQUENCE
        for command in INIT_SEQUENCE:
            await client.write_gatt_char(CHARACTERISTIC_UUID, command)

        # Receive notifications
        await client.start_notify(CHARACTERISTIC_UUID, handle_rx)

        # # Start the device
        await send_cmd(client, CMDS["start"], "start")
        await send_cmd(client, speed_cmd(2.0), "set_speed")

        # Query information
        while True:
            for name, query in INFO_QUERIES.items():
                await send_cmd(client, query, name)

loop = asyncio.get_event_loop()
loop.run_until_complete(run(DEVICE_ADDRESS))
