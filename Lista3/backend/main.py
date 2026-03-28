import os
import random

from fastapi import FastAPI
from fastapi_mqtt import MQTTConfig, FastMQTT
from starlette.middleware.cors import CORSMiddleware
import requests

import pandas as pd

app = FastAPI()

mqtt_config = MQTTConfig(
    host="iot-mqtt",
    port=1883,
    keepalive=60,
)
mqtt = FastMQTT(config=mqtt_config)
mqtt.init_app(app)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

def csv_to_json(file, separator):
    df = pd.read_csv(file, sep=separator, encoding='cp1250')
    return df.head(10).to_json(orient='records', indent=4, force_ascii=False)


@app.get("/")
def main():
    return {"message": "Hello World"}


@app.get("/5G_Dataset")
def get_5G_Dataset(data_source:str = "https://bip.uke.gov.pl/download/gfx/bip/pl/defaultaktualnosci/140/5/111/pozwolenia_ntc_h_2026-01-28.csv"):
    random_num = random.randint(1, 1000000000)
    try:
        request = requests.get(data_source)
        with open(f"app/data/5G_Dataset_{random_num}.csv", "wb") as file:
            file.write(request.content)
        request.raise_for_status()
    except requests.RequestException as e:
        raise "Failed to fetch data:"

    final_json = csv_to_json(f"app/data/5G_Dataset_{random_num}.csv", ";")

    try:
        os.remove(f"app/data/5G_Dataset_{random_num}.csv")
    except Exception as e:
        print(e)

    return final_json

@app.post("/5G_Dataset/")
def post_5G_Dataset(data_source: str = "https://bip.uke.gov.pl/download/gfx/bip/pl/defaultaktualnosci/140/5/111/pozwolenia_ntc_h_2026-01-28.csv", where_to_send: str = "http://localhost:8000/5G_Dataset"):
    try:
        request = requests.get(data_source)
        with open("app/data/5G_Dataset.csv", "wb") as file:
            file.write(request.content)
        request.raise_for_status()

    except requests.RequestException as e:
        raise "Failed to fetch data:"
    data = csv_to_json("app/data/5G_Dataset.csv", ";")
    response = requests.post(where_to_send, json=data)
    return response.json()




@app.get("/5G_Dataset/publish")
async def publish_5G_Dataset(topic: str = "5G_Dataset", data_source:str="https://bip.uke.gov.pl/download/gfx/bip/pl/defaultaktualnosci/140/5/111/pozwolenia_ntc_h_2026-01-28.csv"):
    try:
        request = requests.get(data_source)
        with open("app/data/5G_Dataset.csv", "wb") as file:
            file.write(request.content)
        request.raise_for_status()

    except requests.RequestException as e:
        raise "Failed to fetch data:"
    data = csv_to_json("app/data/5G_Dataset.csv", ";")
    mqtt.publish(topic, data)

@mqtt.on_message()
async def handle_message(client, topic, payload, qos, properties):
    print(f"Received message on topic {topic}: {payload.decode()}")
    return payload.decode()

@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe("5G_Dataset")