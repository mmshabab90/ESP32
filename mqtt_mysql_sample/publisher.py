import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect('localhost', 5252)

while True:
    client.publish('TESTtopic/test', input('Message: '))