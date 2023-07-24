from flask import Flask, render_template, request, Response
from djitellopy import Tello
import threading
import time
import cv2
import sqlite3

conn = sqlite3.connect("database.db")

c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS user
             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
              name TEXT NOT NULL UNIQUE, 
              password TEXT NOT NULL)''')

app = Flask(__name__)
tello = Tello()


def register(name, password):
    try:

        c.execute('''INSERT INTO user (name, password)
                     VALUES (?, ?)''', (name, password))
        conn.commit()

    except sqlite3.IntegrityError:
        print("The user already exists")

def login(name, password):
    c.execute('''SELECT * FROM user WHERE name = ? AND password = ?''', (name, password))
    user = c.fetchone()
    if user:
        print("Anmeldung erfolgreich!")
        return user
    else:
        print("Wrong username or password!")


def video_feed():
    while True:
        frame = tello.get_frame_read().frame
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed_route():
    return Response(video_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

def drone_control():
    while True:
        if 'command' in request.form:
            command = request.form['command']
            if command == 'takeoff':
                tello.takeoff()
            elif command == 'land':
                tello.land()
            elif command == 'up':
                tello.move_up(35)
            elif command == 'down':
                tello.move_down(35)
            elif command == 'forward':
                tello.move_forward(35)
            elif command == 'backward':
                tello.move_backward(35)
            elif command == 'left':
                tello.move_left(35)
            elif command == 'right':
                tello.move_right(35)
            elif command == 'rotate_left':
                tello.rotate_counter_clockwise(35)
            elif command == 'rotate_right':
                tello.rotate_clockwise(35)

def start_drone_thread():
    tello.connect()
    tello.streamon()
    time.sleep(2)
    drone_thread = threading.Thread(target=drone_control)
    drone_thread.start()

if __name__ == '__main__':
    start_drone_thread()
    app.run(debug=True)
