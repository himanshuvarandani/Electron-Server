import hashlib
import re

from app import app
from app.database import db
from app.database.models.students import Students
from fastapi import Depends, Response, status
from fastapi_jwt_auth import AuthJWT
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


@app.post("/students/login")
async def students_login(
    body: RequestBody, response: Response, Auth: AuthJWT = Depends()
):
    email = body.email
    password = hashlib.sha256(str.encode(body.password)).hexdigest()

    result = db.query(Students).filter_by(email=email, password_hash=password).first()
    if not result:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"result": "fail", "reason": "Incorrect credentials"}

    token = Auth.create_access_token(
        subject=result.id, user_claims={"role": "student"}, expires_time=False
    )
    return {"access_token": token}
