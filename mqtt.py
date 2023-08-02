import paho.mqtt.client as mqtt
from database.mongodb import MongoDb

db = MongoDb().db()

#----- MQTT ------------------

def on_connect(client,userdata,flags,rc):
    print(f"Cliente conectado con el código de resultado: {rc}")
    client.subscribe("Sensores/#")

def on_message(client,userdata,msg):

    nombre = msg.topic.split("/")[1]
    estado = msg.payload.decode()
    sensor = db.sensores.find_one({"nombre": nombre})
    if sensor:
        if sensor["estado"] != estado:
            db.sensores.update_one({"nombre": nombre}, {"$set": {"estado":msg.payload.decode()}})

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost",1883,60)
client.loop_forever()