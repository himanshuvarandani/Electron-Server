from app import app
from app.database import db
from app.database.models.submissions import Submissions
from app.database.models.student_subject_map import StudentSubjectMap
from fastapi import Depends, Response, status
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel


class RequestBody(BaseModel):
    attachement: str
    assignment_id: int


@app.get("/student/{student_id}/submission")
async def get_submitted_assignment(
    student_id, assignment_id: int, response: Response, Auth: AuthJWT = Depends()
):
    Auth.jwt_required()

    submission = (
        db.query(Submissions)
            .filter(Submissions.student_id == student_id)
            .filter(Submissions.assignment_id == assignment_id)
            .first()
    )

    if not submission:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"result": "fail", "reason": "No assignment submission found"}

    return submission


# Only allow teachers to post announcements
@app.post("/students/{student_id}/assignment")
async def submit_assignment(
    student_id, body: RequestBody, response: Response, Auth: AuthJWT = Depends()
):
    Auth.jwt_required()

    submission = Submissions()
    submission.attachement = body.attachement
    submission.student_id = body.student_id
    submission.assignment_id = body.assignment_id

    try:
        db.add(submission)
        db.commit()
    except Exception as e:
        response.status_code = status.HTTP_503_UNAVAILABLE
        return {"result": "fail", "reason": str(e)}

    return {"result": "ok"}
