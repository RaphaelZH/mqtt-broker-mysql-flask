import mysql.connector

from flask import Flask

import os

app = Flask(__name__)

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


@app.route("/")
def index():
    return "Hello from Flask!"


@app.route("/databases")
def list_databases():
    try:
        db_connection = connect_to_mysql()
        with db_connection.cursor() as cursor:
            cursor.execute("SHOW DATABASES;")
            databases = cursor.fetchall()
        db_connection.close()
        return {"databases": [db["Database"] for db in databases]}
    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
    
    

"""
import paho.mqtt.client as mqtt

import mysql.connector

import json
import os
import time

MQTT_BROKER_HOST = os.getenv("MQTT_BROKER_HOST")
MQTT_BROKER_PORT = os.getenv("MQTT_BROKER_PORT")

# Get database credentials from environment variables
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")


def handle_telemetry(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)

    sql = "INSERT INTO heartbeat_records (datetime, heart_rate) VALUES (%s, %s)"
    val = (payload["datetime"], payload["heart_rate"])
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe("heart_rate/topic")
    client.on_message = handle_telemetry


def on_message(client, userdata, message):
    print(f"Received message: {message.payload.decode()} on topic {message.topic}")


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


try:
    db_connection = connect_to_mysql()
    with db_connection.cursor() as cursor:
        cursor.execute("SHOW DATABASES;")
        databases = cursor.fetchall()
    db_connection.close()
    print({"databases": [db["Database"] for db in databases]})
except Exception as e:
    print({"error": str(e)}, 500)

# Execute the CREATE DATABASE IF NOT EXISTS statement
# sql_query = "CREATE DATABASE IF NOT EXISTS heartbeat_monitor"
# mycursor.execute(sql_query)
# mydb.database = "heartbeat_monitor"
#
# mycursor.execute(
#    "CREATE TABLE IF NOT EXISTS heartbeat_records (datetime VARCHAR(255), heart_rate INT)"
# )
# mycursor.execute("DROP TABLE IF EXISTS iot_devices")
# mycursor.execute("SHOW TABLES")
# for x in mycursor:
#    print(x)
#    mycursor.execute("SHOW COLUMNS FROM heartbeat_records")
#    for col in mycursor:
#        print("Column:", col)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)

client.loop_start()

while True:
    time.sleep(5)
"""