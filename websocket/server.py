#this is originally for my chicken coop but shouldn't be hard simply to simply have server send video streams to the other clients connected
#I'd like it so that the client sends in their connection request both type=client and also robot=robotID
#robot in its connection request will send with its predefined robotID
#Needs to be greatly altered to allow this. This code most likely won't work on Hopkins or Home network, I'll set up an aws playground server soon

import asyncio
import websockets
from urllib.parse import urlparse, parse_qs

#stream, client sets
door = set()
door2 = set()
streams = set()
async def start_stream():
    for client in streams:
        await client.send('start')
async def stop_stream():
    for client in streams:
        await client.send('stop')

async def handler(websocket, path):

    query = urlparse(path).query
    params = parse_qs(query)

    if 'type' in params and params['type'][0] == 'client':
        if len(door) == 0 and len(door2) == 0:
            await start_stream()
            print('starting stream')
        # Default to door set for clients                                                                                                                                                                     
        door.add(websocket)
        print('Client connected')


        try:
            async for message in websocket:
                #Need to change this so that a client which requests a robot stream
                #might be able to just get rid of this as a whole, client shouldn't be sending messages over website after starting
                if message == 'door2':
                    if websocket in door:
                        door.remove(websocket)
                    door2.add(websocket)
                    print('switched to door 2')
                elif message == 'door':
                    if websocket in door2:
                        door2.remove(websocket)
                    door.add(websocket)
                    print('switched to door 1')

        finally:
            door.discard(websocket)
            door2.discard(websocket)
            if len(door) == 0 and len(door2) == 0:
                await stop_stream()
                print('streams stopped')
            print('Client disconnected:')

    elif 'type' in params and params['type'][0] == 'stream':
        streams.add(websocket)
        stream_name = params['name'][0] if 'name' in params else None
        print('connected ' + str(stream_name))
        if stream_name == 'door':
            async for message in websocket:
                for client in door:
                    if client != websocket:
                        await client.send(message)
        elif stream_name == 'door2':
            async for message in websocket:
                for client in door2:
                    if client != websocket:
                        await client.send(message)

async def main():
    #8765 is classic websocket port
    server = await websockets.serve(handler, "localhost", 8765)
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
