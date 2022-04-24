from app import app
from app.database import db
from app.database.models.announcements import Announcements
from fastapi import Depends, Response
from fastapi_jwt_auth import AuthJWT


@app.get("/subjects/{subject_id}/announcements")
async def get_subject_announcements(
    subject_id, response: Response, Auth: AuthJWT = Depends()
):
    Auth.jwt_required()

    announcements = (
        db.query(Announcements).filter(Announcements.subject_id == subject_id).all()
    )

    return announcements
