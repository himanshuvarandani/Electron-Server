from app import app
from app.database import db
from app.database.models.subject_class_map import SubjectClassMap
from app.database.models.timetable import Timetable
from fastapi import Depends, Response, status
from fastapi_jwt_auth import AuthJWT


@app.get("/classes/{class_id}/timetable")
async def class_timetable(class_id, response: Response, Auth: AuthJWT = Depends()):
    Auth.jwt_required()

    timetables = (
        db.query(Timetable)
            .join(SubjectClassMap, SubjectClassMap.class_id == class_id)
            .filter(Timetable.subject_id == SubjectClassMap.subject_id)
            .all()
    )

    if not timetables:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"result": "fail", "reason": "No timetable found"}

    return timetables
