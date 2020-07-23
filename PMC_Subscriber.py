import paho.mqtt.client as mqtt

# This is the Subscriber

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("topic/test")

def on_message(client, userdata, msg):
#    while true:
    if msg.payload.decode() == "full":
        print("Bin ID:3 Full, Please empty the bin!")
    elif msg.payload.decode() == "nfull":
        print("Bin ID:3 Not Full, Bin is at safe state to throw grabage !")
#        client.disconnect()
    
client = mqtt.Client()
client.connect("127.0.1.1",1883,60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()
