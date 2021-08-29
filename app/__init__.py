from fastapi import FastAPI

app = FastAPI()

from app import routes

@app.get("/")
def home():
  return {"status": "OK"}
