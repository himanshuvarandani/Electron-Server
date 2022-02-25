from app import app
from app.database import db
from app.database.models.timetable import Timetable
from fastapi import Response, status


@app.get("/classes/{class_id}/timetable")
async def class_timetable(class_id, response: Response):
    timetable = db.query(Timetable).filter(Timetable.class_id == class_id).all()

    if not timetable:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"result": "fail", "reason": "No timetable found"}

    return timetable
