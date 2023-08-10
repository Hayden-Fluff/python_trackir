import asyncio
import websockets
import tkinter
import time
from trackir import TrackIRDLL


trackIr = TrackIRDLL(tkinter.Tk().wm_frame())
sendingData = False
dataFrequency = float(0.1)
#0.00833 = 120hz, 0.0166 = 60hz
parsedTrackIRData = trackIr.NP_GetData()


async def Main(websocket):
    global sendingData
    global dataFrequency

    name = await websocket.recv()

    #if name == "GetData":
    #    await websocket.send(str(trackIr.NP_GetData))
    #    print("Sent TrackIR data")

    if name == "GetDataSnapshot":
        await websocket.send(str(trackIr.NP_GetData()))
        print("Sent raw data snapshot")
        print(trackIr.NP_GetData())

    if name == "StartData":
        sendingData = True
        await websocket.send("Started")
        print("Started sending TrackIR data")

    if name == "StopData":
        sendingData = False
        await websocket.send("Stopped")
        print("Stopped sending TrackIR data")

    if "DataFrequency" in name:
        var = name.replace("DataFrequency:", '')
        dataFrequency = float(var)
        print("Set DataFrequency to " + var)
        
        
    while sendingData:
        await websocket.send(str(trackIr.NP_GetData()))
        await asyncio.sleep(dataFrequency)


async def main():
    async with websockets.serve(Main, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())