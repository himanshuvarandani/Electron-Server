from app import app
from app.database import db
from app.database.models.subjects import Subjects
from fastapi import Depends, Response, status
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel


@app.get("/subjects/{subject_id}")
async def get_subject_details(
    subject_id: int, response: Response, Auth: AuthJWT = Depends()
):
    Auth.jwt_required()

    subject = db.query(Subjects).filter(Subjects.id == subject_id).first()

    if not subject:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"result": "fail", "reason": "No subject found"}

    return subject