import asyncio
from bleak import BleakClient

DEVICE_ADDRESS = "XX:XX:XX:XX:XX:XX"  # Replace with your device's address
CHARACTERISTIC_UUID = "49535343-026E-3A9B-954C-97DAEF17E26E"  # Example characteristic
# 968C8C0A-BFD0-EBCD-E5E0-A0CB16F0BFE9
# identifier:		968C8C0A-BFD0-EBCD-E5E0-A0CB16F0BFE9
# Local Name:	LifeSpan
# Tx Power:		0

INIT_SEQUENCE = [
    b"\x02\x00\x00\x00\x00",
    b"\xC2\x00\x00\x00\x00",
    b"\xE9\xFF\x00\x00\x00",
    b"\xE4\x00\xF4\x00\x00"
]

INFO_QUERIES = {
    "unknown":  b"\xA1\x81\x00\x00\x00",
    "steps":    b"\xA1\x88\x00\x00\x00",
    "calories": b"\xA1\x87\x00\x00\x00",
    "distance": b"\xA1\x85\x00\x00\x00",
    "time":     b"\xA1\x89\x00\x00\x00",
    "speed":    b"\xA1\x82\x00\x00\x00"
}

async def run(address):
    async with BleakClient(address) as client:
        # Write INIT_SEQUENCE
        for command in INIT_SEQUENCE:
            await client.write_gatt_char(CHARACTERISTIC_UUID, command)
        
        # Query information
        for name, query in INFO_QUERIES.items():
            await client.write_gatt_char(CHARACTERISTIC_UUID, query)
            response = await client.read_gatt_char(CHARACTERISTIC_UUID)
            print(f"{name}: {response}")

loop = asyncio.get_event_loop()
loop.run_until_complete(run(DEVICE_ADDRESS))
