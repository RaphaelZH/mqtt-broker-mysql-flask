## Running Mosquitto with Docker

The basic Docker command gets Mosquitto running with proper port mapping and volume mounts.

```
docker run -d \
  --name mosquitto \
  -p 1883:1883 \
  -v $(pwd)/mosquitto/config:/mosquitto/config \
  -v $(pwd)/mosquitto/data:/mosquitto/data \
  -v $(pwd)/mosquitto/log:/mosquitto/log \
  eclipse-mosquitto:latest
```
