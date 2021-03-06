from app import app
from app.database import db
from app.database.models.assignments import Assignments
from app.database.models.calendar import Calendar
from app.database.models.submissions import Submissions
from app.database.models.teacher_subject_map import TeacherSubjectMap
from fastapi import Depends, Response, status
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel


class AssignmentRequestBody(BaseModel):
    title: str
    body: str
    attachement: str
    end_date: str
    max_marks: int
    teacher_id: int


class SubmissionsRequestBody(BaseModel):
    marks: int
    student_id: int
    teacher_id: int


# Only allow teachers to post assignments
@app.post("/subjects/{subject_id}/assignment")
async def post_subject_assignment(
    subject_id,
    body: AssignmentRequestBody,
    response: Response,
    Auth: AuthJWT = Depends(),
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

    assignment = Assignments()
    assignment.title = body.title
    assignment.body = body.body
    assignment.attachement = body.attachement
    assignment.end_date = body.end_date
    assignment.max_marks = body.max_marks
    assignment.subject_id = subject_id
    assignment.teacher_id = body.teacher_id

    calendar = Calendar()
    calendar.deadline = body.end_date
    calendar.task = "Assignment " + body.title
    calendar.subject_id = subject_id

    try:
        db.add(assignment)
        db.add(calendar)
        db.commit()
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"result": "fail", "reason": str(e)}

    return {"result": "ok"}


# Only allow teachers to give marks
@app.post("/assignments/{assignment_id}/update-marks")
async def update_assignment_marks(
    assignment_id, body: SubmissionsRequestBody, response: Response, Auth: AuthJWT = Depends()
):
    Auth.jwt_required()

    try:
        db.query(Submissions) \
            .filter(Submissions.student_id == body.student_id) \
            .filter(Submissions.assignment_id == body.assignment_id) \
            .update({ 'marks': body.marks, 'teacher_id': body.teacher_id })
        db.commit()
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"result": "fail", "reason": str(e)}

    return {"result": "ok"}


# to get all submissions of an assignment for teacher
@app.get("/assignments/{assignment_id}/submissions")
async def get_assignment_submissions(
    assignment_id, response: Response, Auth: AuthJWT = Depends()
):
    Auth.jwt_required()

    assignments = db.query(Submissions).filter(Submissions.assignment_id == assignment_id).all()

    return assignments
