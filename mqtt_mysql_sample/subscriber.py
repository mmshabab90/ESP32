import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect('localhost', 5252)

def on_connect(client, userdata, flags, rc):
    print('Connected to a broker!')
    client.subscribe('TESTtopic/test')
    
def on_message(client, userdata, message):
    print(message.payload.decode())
    
while True:
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()