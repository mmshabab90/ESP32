import wifimgr
from machine import Pin, ADC
from time import sleep
from umqtt.simple import MQTTClient

wlan = wifimgr.get_connection()
if wlan is None:
    print("Could not initialize the network connection.")
    while True:
        pass  # you shall not pass :D


# Main Code goes here, wlan is a working network.WLAN(STA_IF) instance.
print("ESP OK")

SERVER = "mqtt.thingspeak.com"
client = MQTTClient("umqtt_client", SERVER)

CHANNEL_ID = "931555"
WRITE_API_KEY = "J51OFKLW80P3WX6W"

topic = "channels/" + CHANNEL_ID + "/publish/" + WRITE_API_KEY

led_1 = Pin(18, Pin.OUT)
led_2 = Pin(19, Pin.OUT)

sensor_1 = ADC(Pin(34))
sensor_1.atten(ADC.ATTN_11DB)
sensor_1.width(ADC.WIDTH_9BIT)

sensor_2 = ADC(Pin(35))
sensor_2.atten(ADC.ATTN_11DB)
sensor_2.width(ADC.WIDTH_9BIT)

threshold = 30

while True:
    sensor_1_val = sensor_1.read()
    sensor_2_val = sensor_2.read()
    
    if (sensor_1_val < threshold) or (sensor_2_val < threshold):
      pass
        
    if (sensor_1_val > threshold) or (sensor_2_val > threshold):
        print('Sensor 1 = ' + str(sensor_1_val))
        print('Sensor 2 = ' + str(sensor_2_val))
        
        payload = "field1="+str(sensor_1_val)+"&field2="+str(sensor_2_val)
        
        client.connect()
        client.publish(topic, payload)
        client.disconnect()
    
    if (sensor_1_val >= threshold):
        led_1.value(1)
    else:
        led_1.value(0)
    
    if (sensor_2_val >= threshold):
        led_2.value(1)
    else:
        led_2.value(0)
sleep(0.0000003)



