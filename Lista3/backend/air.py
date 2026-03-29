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
@app.post("/ETDataset")
async def post_ETDataset(
    request: Request,
    packages_amount: int = 100,
):
    body = await request.json()
    data_source = body.get(
        "data_source",
        "https://raw.githubusercontent.com/zhouhaoyi/ETDataset/refs/heads/main/ETT-small/ETTh1.csv",
    )
    where_to_send = body.get("address", "http://iot-reciever:8001/")
    repeat_interval = float(body.get("repeat_interval", 0.5))
    from_req_to_file("app/data/ETDataset.csv", data_source)
    separator = body.get("separator", ";")

    for i in range(packages_amount):
        data = csv_to_json("app/data/ETDataset.csv", separator, i)
        response = requests.post(where_to_send, json=data)
        await asyncio.sleep(repeat_interval)

    return response.json()


@app.get("/ETDataset")
def get_ETDataset(
    data_source: str = "https://raw.githubusercontent.com/zhouhaoyi/ETDataset/refs/heads/main/ETT-small/ETTh1.csv",
    separator: str = ";",
):
    from_req_to_file("app/data/ETDataset.csv", data_source)
    df = pd.read_csv(
        "app/data/ETDataset.csv", sep=separator, encoding="cp1250", header=0
    )

    return df.to_json(orient="records")


@app.get("/ETDataset/columns")
def get_ETDataset_columns(
    data_source: str = "https://raw.githubusercontent.com/zhouhaoyi/ETDataset/refs/heads/main/ETT-small/ETTh1.csv",
    separator: str = ";",
):
    from_req_to_file("app/data/ETDataset.csv", data_source)
    df = pd.read_csv(
        "app/data/ETDataset.csv", sep=separator, encoding="cp1250", header=0
    )
    return df.columns.tolist()


# ============= MQTT
@app.post("/ETDataset/publish")
async def publish_ETDataset(request: Request):
    body = await request.json()
    data_source = body.get(
        "data_source",
        "https://raw.githubusercontent.com/zhouhaoyi/ETDataset/refs/heads/main/ETT-small/ETTh1.csv",
    )
    repeat_interval = float(body.get("repeat_interval", 0.5))
    topic = body.get("topic", "ETDataset")

    from_req_to_file("app/data/ETDataset.csv", data_source)
    for i in range(100):
        data = csv_to_json("app/data/ETDataset.csv", ",", i)
        mqtt.client.publish(topic, data)
        print(repeat_interval, flush=True)
        await asyncio.sleep(repeat_interval)

    return {"message": "ETDataset finished"}


@app.post("/add_topic")
def add_subscription(topic: str):
    mqtt.client.subscribe(topic)
    return {"message": f"Subscribed to topic: {topic}"}


@mqtt.on_connect()
def handle_connect(client, flags, rc, properties):
    mqtt.client.subscribe("ETDataset")
