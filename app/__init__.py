from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

from app import routes

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
  expose_headers=["*"],
)

@app.get("/")
def home():
  return {"status": "OK"}
