from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .database.database import db_manager
from . import models
app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


print("working")
models.Base.metadata.create_all(bind=db_manager.engine)

@app.get("/")
def main():
    return {"message": "Hello World"}