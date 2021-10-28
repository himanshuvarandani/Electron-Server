import re
from app import app
from fastapi import Response
from pydantic import BaseModel, validator

class RequestBody(BaseModel):
  email: str
  password: str

  @validator('email')
  def validate_email(cls, v):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    if not re.fullmatch(regex, v):
      raise ValueError
    return v

@app.post("/student/login")
async def student_login(body: RequestBody, response: Response):
  email = body.email
  password = body.password
  
  if email == "test@gmail.com" and password == "pass":
    return {"token": "4hbjn434jb234vjb"}
  
  return {}
