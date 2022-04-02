import re

from app import app
from app.database import db
from app.database.models.teachers import Teachers
from fastapi import Depends, Response, status
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel, validator
from werkzeug.security import check_password_hash


class RequestBody(BaseModel):
    email: str
    password: str

    @validator("email")
    def validate_email(cls, v):
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

        if not re.fullmatch(regex, v):
            raise TypeError("Invalid Email")
        return v


@app.post("/teachers/login")
async def teachers_login(
    body: RequestBody, response: Response, Auth: AuthJWT = Depends()
):
    result = db.query(Teachers).filter_by(email=body.email).first()
    if not result:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"result": "fail", "reason": "Incorrect credentials"}

    if not check_password_hash(result.password_hash, body.password):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"result": "fail", "reason": "Incorrect credentials"}

    token = Auth.create_access_token(
        subject=result.id, user_claims={"role": "teacher"}, expires_time=False
    )
    return {"access_token": token}
