import os
import random

from fastapi import FastAPI, Request
from fastapi_mqtt import MQTTConfig, FastMQTT
from starlette.middleware.cors import CORSMiddleware
import requests
import docker
import pandas as pd
from fastapi.responses import StreamingResponse

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
# ========== showing container logs on site

docker_client = docker.from_env()
container = docker_client.containers.get("iot-reciever")


@app.get("/logs")
def get_logs():
    return StreamingResponse(
        container.logs(stream=True, follow=True), media_type="text/text"
    )


# ========== REST
@app.post("/")
async def main(request: Request):
    body = await request.json()
    print(body)
    return body


@app.post("/different")
async def main(request: Request):
    print("Sprawdzenie czy działa przekierowanie")
    body = await request.json()
    return {"odebrano_body": body}


# ===================== MQTT
topics = {"ETDataset"}


@app.get("/topics")
def get_topics():
    return {"topics": list(topics)}


@app.post("/add_topic")
def add_subscription(topic: str):
    mqtt.client.subscribe(topic)
    topics.add(topic)
    return {"message": "Subscribed to topic"}


@mqtt.on_message()
async def handle_message(client, topic, payload, qos, properties):
    print(f"Received message on topic {topic}: {payload.decode()}", flush=True)
    return payload.decode()


@mqtt.on_connect()
def handle_connect(client, flags, rc, properties):
    mqtt.client.subscribe("ETDataset")
