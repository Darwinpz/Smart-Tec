import pytesseract as ts
import paho.mqtt.client as mqtt
from database.mongodb import MongoDb
import requests
import time
import shutil
import uuid
from PIL import Image

ts.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

db = MongoDb().db()

#----- MQTT ------------------

def on_connect(client,userdata,flags,rc):
    print(f"Cliente conectado con el código de resultado: {rc}")
    client.subscribe("Sensores/#")

def on_message(client,userdata,msg):

    nombre = msg.topic.split("/")[1]

    if "SENSOR" in nombre:
        estado = msg.payload.decode()
        sensor = db.sensores.find_one({"nombre": nombre})
        if sensor:
            if sensor["estado"] != estado:
                db.sensores.update_one({"nombre": nombre}, {"$set": {"estado":msg.payload.decode()}})
    if "PUSH" in nombre:                
        enlace='http://192.168.3.120'
        url = './static/img/placas/'+str(uuid.uuid1())+'.jpg'
        response = requests.get(f'{enlace}/capture?_cb={int(round(time.time() * 1000))}', stream=True)
        with open(url, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        imagen = Image.open(url)
        text = ts.image_to_string(imagen)
        print(text)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost",1883,60)
client.loop_forever()