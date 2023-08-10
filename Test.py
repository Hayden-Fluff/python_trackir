import asyncio
import websockets

var = int(0)

async def Main(websocket):
    global var
    while True:
        var = var + 1
        await websocket.send(str(var))
        await asyncio.sleep(0.02)

async def main():
    async with websockets.serve(Main, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())