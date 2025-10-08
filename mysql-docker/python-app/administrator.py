import mysql.connector

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import threading

import os
import time

app = Flask(__name__)
app.config["SECRET_KEY"] = "123456"  # Replace with a strong secret key
socketio = SocketIO(app)
thread_lock = threading.Lock()

# Get database credentials from environment variables
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")


def connect_to_mysql():
    try:
        return mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            port=3306,
        )
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None


def random_heart_rate():
    return 60 + int(40 * os.urandom(1)[0] / 255)  # Random heart rate between 60 and 100


@app.route("/")
def index():
    return render_template("index.html", title="Heartbeat Monitor")


def background_thread():
    sql = "INSERT INTO heartbeat_records (datetime, heart_rate) VALUES (%s, %s)"
    while True:
        heart_rate = random_heart_rate()
        val = (time.strftime("%Y-%m-%d %H:%M:%S"), heart_rate)
        my_cursor.execute(sql, val)
        print(my_cursor.rowcount, "record inserted.")
        
        # Generate or fetch the value you want to update
        my_cursor.execute(
            "SELECT heart_rate FROM heartbeat_records ORDER BY datetime DESC LIMIT 1;"
        )
        result = my_cursor.fetchone()
        heart_rate = result[0]
        socketio.emit("update_value", {"heart_rate": heart_rate})
        print(heart_rate)
        socketio.sleep(2)  # Update every second


@socketio.on("connect")
def test_connect():
    print("Client connected")
    # Start the background thread if it's not already running
    if (
        not hasattr(socketio, "background_thread_running")
        or not socketio.background_thread_running
    ):
        socketio.start_background_task(target=background_thread)
        socketio.background_thread_running = True


@socketio.on("disconnect")
def test_disconnect():
    print("Client disconnected")


if __name__ == "__main__":
    if db_connection := connect_to_mysql():
        print("Successfully connected to MySQL!")
    else:
        print("Failed to connect to MySQL.")

    db_connection = connect_to_mysql()
    db_connection.autocommit = True
    my_cursor = db_connection.cursor()
    my_cursor.execute(
        "CREATE TABLE IF NOT EXISTS heartbeat_records (datetime VARCHAR(255), heart_rate INT)"
    )
    db_connection.database = "heartbeat_monitor"
    db_connection.table = "heartbeat_records"

    app.run(host="0.0.0.0", port=5000, debug=True)

    while True:
        time.sleep(2)
