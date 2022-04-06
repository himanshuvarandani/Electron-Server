from app import app
from app.database import db
from app.database.models.calendar import Calendar
from fastapi import Depends, Response, status
from fastapi_jwt_auth import AuthJWT


@app.get("/classes/{class_id}/calendar")
async def class_timetable(class_id, response: Response, Auth: AuthJWT = Depends()):
    Auth.jwt_required()

    calendar = db.query(Calendar).filter(Calendar.class_id == class_id).all()

    if not calendar:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"result": "fail", "reason": "No calendar found"}

    return calendar
