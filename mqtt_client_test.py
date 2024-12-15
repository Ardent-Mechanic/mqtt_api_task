import paho.mqtt.client as mqtt

from config import settings

# MQTT_BROKER = "dev.rvts.ru"  # Адрес вашего брокера
# MQTT_PORT = 1883  # Порт брокера
# MQTT_TOPIC = "sensor/802241/data"  # Тема для подписки/публикации


# Типо база данных
message = []


# Callback при подключении
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(settings.mqtt_config.topic)


# Callback при получении сообщения
def on_message(client, userdata, msg):
    global message
    print(f"Received message: {msg.payload.decode()} on topic: {msg.topic}")
    message.append({"topic": msg.topic, "message": msg.payload.decode()})


# Создание MQTT клиента
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
