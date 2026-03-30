import os
import random
import time
import asyncio
import zipfile
import csv
import json
from fastapi import FastAPI, Response, Request
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


source = os.getenv("DATA_SOURCE")
save_path = os.getenv("SAVE_PATH")
sep = os.getenv("SEPARATOR")
interval = os.getenv("REPEAT_INTERVAL")
tpc = os.getenv("TOPIC")
print(f"DEBUG: Odczytany topic z OS: {tpc}")
def csv_to_json(file, separator, index=0):
    df = pd.read_csv(file, sep=separator, encoding="cp1250", header=0)
    if index is not None:
        row = df.iloc[index]
    else:
        row = df

    return row.to_json(indent=4, force_ascii=False)


def from_req_to_file(file_path, data_source):
    try:
        request = requests.get(data_source)
        print(data_source, flush=True)
        with open(file_path, "wb") as file:
            file.write(request.content)
        request.raise_for_status()
    except requests.RequestException as e:
        raise f"Failed to fetch data: {e}"


# ============= REST
@app.post("/solar")
async def post_solar(
    request: Request,
    packages_amount: int = 100,
):
    body = await request.json()
    data_source = body.get(
        "data_source",
        source,
    )
    where_to_send = body.get("address", "http://iot-reciever:8001/")
    repeat_interval = float(body.get("repeat_interval", interval))
    from_req_to_file(save_path, data_source)
    separator = body.get("separator", sep)

    for i in range(packages_amount):
        data = csv_to_json(save_path, separator, i)
        response = requests.post(where_to_send, json=data)
        await asyncio.sleep(repeat_interval)

    return response.json()


@app.get("/solar")
def get_solar(
    data_source: str = source,
    separator: str = sep,
):
    from_req_to_file(save_path, data_source)
    df = pd.read_csv(
        save_path, sep=separator, encoding="cp1250", header=0
    )

    return df.head(50).to_json(orient="records")


@app.get("/solar/columns")
def get_solar_columns(
    data_source: str = source,
    separator: str = sep,
):
    from_req_to_file(save_path, data_source)
    df = pd.read_csv(
        save_path, sep=separator, encoding="cp1250", header=0
    )
    return df.columns.tolist()


# ============= MQTT
@app.post("/solar/publish")
async def publish_solar(request: Request):
    body = await request.json()
    data_source = body.get(
        "data_source",
        source,
    )
    repeat_interval = float(body.get("repeat_interval", interval))
    print("ssssssss")
    print(tpc)
    topic = body.get("topic", tpc)

    from_req_to_file(save_path, data_source)
    for i in range(100):
        data = csv_to_json(save_path, ",", i)
        mqtt.client.publish(topic, data)
        print(repeat_interval, flush=True)
        await asyncio.sleep(repeat_interval)

    return {"message": "solar finished"}


@app.post("/add_topic")
def add_subscription(topic: str):
    mqtt.client.subscribe(topic)
    return {"message": f"Subscribed to topic: {topic}"}


@mqtt.on_connect()
def handle_connect(client, flags, rc, properties):
    print(tpc, flush=True)
    mqtt.client.subscribe(tpc)
