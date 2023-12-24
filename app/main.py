from flask import Flask
from flask_socketio import SocketIO, emit
import asyncio
import cv2
from pynput import mouse
from pynput.mouse import Listener as MouseListener
import base64
import serial
from common.serial_helper import find_serial_port
from services import main_service
from routers.main_router import main_blueprint
from database.data import create_database
import websockets


create_database()
app = Flask(__name__, template_folder='static/html')
app._static_folder = 'static'
app.register_blueprint(main_blueprint)

port = find_serial_port()
if port[1] == 'Windows':
    ser = serial.Serial('COM1', 9600)
elif port[1] == 'Linux':
    ser = serial.Serial('/dev/ttyUSB0', 9600)

socketio = SocketIO(app)

async def capture_webcam_image(cap):
    try:
        while True:
            ret, frame = cap.read()

            if ret and frame is not None:
                _, img_encoded = cv2.imencode('.jpg', frame)
                img_bytes = img_encoded.tobytes()
                img_base64 = base64.b64encode(img_bytes).decode('utf-8')
                await asyncio.sleep(1)
                socketio.emit('update_webcam', {'image': img_base64})
                main_service.save_mouse_data(None, None, img_bytes)
            else:
                print("Error: Unable to capture from the webcam.")
                break
    except Exception as e:
        print(f'Error capturing webcam: {e}')
    finally:
        cap.release()


def read_serial():
    try:
        while True:
            ret, frame = cap.read()
            if ret:
                _, img_encoded = cv2.imencode('.jpg', frame)
                img_bytes = img_encoded.tobytes()
                img_base64 = base64.b64encode(img_bytes).decode('utf-8')
                socketio.emit('mouse_data', {'x': 0, 'y': 0})
    except Exception as e:
        print(f"Error reading serial data: {e}")

@socketio.on('update_mouse')
def handle_mouse_update(data):
    x, y = data['x'], data['y']
    emit('update_mouse', {'x': x, 'y': y}, broadcast=True)

async def mouse_data(websocket):
    try:
        while True:
            x, y, img_data = await get_mouse_data(cap)
            await websocket.send(f"{x},{y},{img_data}")
            await asyncio.sleep(1)
    except websockets.exceptions.ConnectionClosed:
        print("Connection closed.")

async def get_mouse_data(cap):
    mouse_controller = mouse.Controller()
    x, y = mouse_controller.position
    ret, frame = cap.read()
    _, img_encoded = cv2.imencode('.jpg', frame)
    img_data = img_encoded.tobytes()
    return x, y, img_data

def on_click(x, y, button, pressed):
    if button == mouse.Button.left and pressed:
        ret, frame = cap.read()
        if ret:
            _, img_encoded = cv2.imencode('.jpg', frame)
            img_bytes = img_encoded.tobytes()
            main_service.save_mouse_data(x, y, img_bytes)
        else:
            print("Error: Unable to capture frame from the webcam.")

if __name__ == '__main__':
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    start_server = websockets.serve(mouse_data, "127.0.0.1", 8001)
    if cap.isOpened():
        asyncio.get_event_loop().create_task(capture_webcam_image(cap))
        with MouseListener(on_click=on_click) as listener:
            socketio.start_background_task(target=read_serial)
            
            socketio.run(app, port=8002, use_reloader=False, debug=True)
    else:
        print("Error: Could not open webcam.")