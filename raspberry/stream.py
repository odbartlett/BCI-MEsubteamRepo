import base64
import websockets





import asyncio

camera = cv2.VideoCapture(0)
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = True
ssl_context.verify_mode = ssl.CERT_REQUIRED
if not camera.isOpened():
    print("Failed to open camera")
    exit()
async def raspberry_pi_client():
    #used code initially using my aws server, will need to provision BCI server to run website and websocket server
    uri = "wss://matthewschricker.me/ws"
    try:
        async with websockets.connect(uri, ssl=ssl_context) as websocket:
            while True:
                ret, frame = camera.read()
                if not ret:
                    print("Failed to capture image")
                    continue

                _, buffer = cv2.imencode('.jpg', frame)
                jpg_as_text = base64.b64encode(buffer).decode('utf-8')
                await websocket.send(jpg_as_text)
    except websockets.exceptions.InvalidStatusCode as e:
        print(f"Connection failed with status code: {e.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

asyncio.run(raspberry_pi_client())
