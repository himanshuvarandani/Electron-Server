from app import app
from datetime import datetime, timedelta
from fastapi import Request
import jwt
from fastapi.responses import JSONResponse

SECRET_KEY = "loadthisfromenv"

@app.post("/student/login")
async def student_login(request: Request):
  body = await request.json()
  u = body["username"]
  p = body["password"]

  payload = {
    "exp": datetime.utcnow()+timedelta(days=0,hours=24),
    "iat": datetime.utcnow(),
  }
  token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
  
  if u == "USERNAME" and p == "PASSWORD":
    content = {"status": "OK"}
    response = JSONResponse(content=content)
    response.headers["X-AUTH-TOKEN"] = f"{token}"
    return response
  
  return {"status": "FAIL"}