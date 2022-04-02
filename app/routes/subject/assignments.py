from app import app
from app.database import db
from app.database.models.assignments import Assignments
from app.database.models.calendar import Calendar
from app.database.models.subject_class_map import SubjectClassMap
from app.database.models.subjects import Subjects
from app.database.models.teacher_subject_map import TeacherSubjectMap
from fastapi import Depends, Response, status
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel


class RequestBody(BaseModel):
    title: str
    body: str
    attachement: str
    end_date: str
    subject_id: int
    teacher_id: int


@app.get("/subjects/{subject_id}/assignments")
async def get_subject_assignments(
    subject_id, response: Response, Auth: AuthJWT = Depends()
):
    Auth.jwt_required()

    assignments = (
        db.query(Assignments).filter(Assignments.subject_id == subject_id).all()
    )

    if not assignments:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"result": "fail", "reason": "No assignments found"}

    return assignments


# Only allow teachers to post assignments
@app.post("/subjects/{subject_id}/assignments")
async def post_subject_assignments(
    subject_id, body: RequestBody, response: Response, Auth: AuthJWT = Depends()
):
    Auth.jwt_required()

    existing = (
        db.query(TeacherSubjectMap)
            .filter(TeacherSubjectMap.subject_id == subject_id)
            .filter(TeacherSubjectMap.teacher_id == body.teacher_id)
            .first()
    )

    if not existing:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"result": "fail", "reason": "Teacher not available in given class"}

    assignment = assignments()
    assignment.title = body.title
    assignment.body = body.body
    assignment.attachement = body.attachement
    assignment.end_date = body.end_date
    assignment.subject_id = subject_id
    assignment.teacher_id = body.teacher_id

    try:
        db.add(assignment)
        
        classes = (
            db.query(SubjectClassMap).filter(SubjectClassMap.subject_id == subject_id).all()
        )

        for class1 in classes:
            calendar = Calendar()
            calendar.deadline = body.end_date
            calendar.task = "Assignment " + body.title
            calendar.subject_id = subject_id
            calendar.class_id = class1.class_id

            db.add(calendar)
        
        db.commit()
    except Exception as e:
        response.status_code = status.HTTP_503_UNAVAILABLE
        return {"result": "fail", "reason": str(e)}

    return {"result": "ok"}
