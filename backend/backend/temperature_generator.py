import json
import random
import time
import paho.mqtt.client as mqtt
from main import receive_temperature

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)
        print(data)
        receive_temperature(data)
    except Exception as e:
        print(f"Error processing MQTT message: {str(e)}")


def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")


def on_publish(client, userdata, mid):
    print(f"Message {mid} published.")

def generate_temperature():
    return round(random.uniform(20, 30), 2)

def publish_temperature(client, topic, payload):
    client.publish(topic, payload=json.dumps(payload))

def main():
    with open('config.json') as config_file:
        config = json.load(config_file)

    devices = config["devices"]
    mqtt_config = config["mqtt"]

    client = mqtt.Client()
    client.username_pw_set(mqtt_config["username"], mqtt_config["password"])
    client.on_message = on_message
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.connect(mqtt_config["broker"], mqtt_config["port"])
    client.subscribe(mqtt_config["topic"])

    client.loop_start()
    while True:
        for device in devices:
            temperature_data = {
               
                "device_name": device["name"],
                "temperature": generate_temperature()
            }
            publish_temperature(client, mqtt_config["topic"], temperature_data)

        time.sleep(60)

if __name__ == "__main__":
    main()
