from app import app
from fastapi import Request

@app.post("/student/login")
async def student_login(request: Request):
  body = await request.json()
  u = body["username"]
  p = body["password"]
  
  if u == "USERNAME" and p == "PASSWORD":
    return {"token": "4hbjn434jb234vjb"}
  
  return {}