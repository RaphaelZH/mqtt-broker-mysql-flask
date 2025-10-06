CREATE DATABASE IF NOT EXISTS heartbeat_monitor;

GRANT ALL PRIVILEGES ON heartbeat_monitor.* TO 'root'@'%' IDENTIFIED BY '123456';
GRANT ALL PRIVILEGES ON heartbeat_monitor.* TO 'raphaelzh'@'%' IDENTIFIED BY '123456';
FLUSH PRIVILEGES;

USE heartbeat_monitor;
GRANT ALL PRIVILEGES ON heartbeat_monitor.* TO 'root'@'%' IDENTIFIED BY '123456';
FLUSH PRIVILEGES;
CREATE TABLE IF NOT EXISTS heartbeat_records (datetime VARCHAR(255), heart_rate INT);