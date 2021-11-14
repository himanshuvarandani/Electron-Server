import re
import hashlib
from app import app
from app.database import db
from app.database.models.teachers import Teachers
from fastapi import Response, status
from pydantic import BaseModel, validator


class RequestBody(BaseModel):
    email: str
    password: str

    @validator("email")
    def validate_email(cls, v):
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

        if not re.fullmatch(regex, v):
            raise TypeError("Invalid Email")
        return v


@app.post("/teacher/login")
async def teacher_login(body: RequestBody, response: Response):
    email = body.email
    password = hashlib.sha256(str.encode(body.password)).hexdigest()

    result = db.query(Teachers).filter_by(email=email, password_hash=password).first()
    if result is None:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"result": "fail", "reason": "Incorrect credentials"}

    return {"result": "ok"}
