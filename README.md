# Flask Webcam Streaming and Mouse Tracking

> This project demonstrates a real-time webcam streaming application using Flask and Socket.IO. It also includes mouse tracking functionality where the mouse coordinates and webcam frames are transmitted to the server and displayed on the client-side.
# Setup


## Clone the repository:


```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

## INSTALL THE PACKAGES
```bash
pip install Flask Flask-SocketIO asyncio opencv-python pynput pyserial websockets sqlite
```

## RUN THE APP FROM THE MAIN
> The application can be launched from the main.py file by clicking F5.

# Project Structure

* **app.py**: The main Flask application file.
* **static/html**: Contains HTML templates for the application.
* **common/serial_helper.py**: Helper functions for finding the serial port.
* **services/main_service.py**: Service functions, including saving mouse data to the database.
* **routers/main_router.py**: Blueprint for defining routes and views.
* **database/data.py**: Functions for creating the SQLite database.

# Usage

- Open a web browser and navigate to http://127.0.0.1:8002.
- The webpage will display mouse coordinates.
- Left-clicking the mouse captures a frame from the webcam and saves the image and mouse coordinates to the database.

# Notes

    The application uses Flask to serve the web interface and Socket.IO for real-time communication.
    Webcam frames are captured using OpenCV, encoded as base64, and transmitted to the client.
    Mouse tracking is implemented using the pynput library, and the coordinates are sent to the server via Socket.IO.
    The SQLite database is used to store mouse coordinates and captured images.