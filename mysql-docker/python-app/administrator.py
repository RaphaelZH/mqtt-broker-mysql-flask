import mysql.connector

from flask import Flask, render_template

import os
import time

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


def random_heart_rate():
    return 60 + int(40 * os.urandom(1)[0] / 255)  # Random heart rate between 60 and 100


@app.route("/", methods=["GET", "POST"])
def index():
    heart_rate = random_heart_rate()
    stop = 0
    return render_template(
        "index.html", title="Heartbeat Monitor", heart_rate=heart_rate, stop=stop
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

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

    sql = "INSERT INTO heartbeat_records (datetime, heart_rate) VALUES (%s, %s)"
    while True:
        heart_rate = random_heart_rate()
        val = (time.strftime("%Y-%m-%d %H:%M:%S"), heart_rate)
        my_cursor.execute(sql, val)
        print(my_cursor.rowcount, "record inserted.")

        time.sleep(5)


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
