from app import app
from app.database import db
from app.database.models.assignments import Assignments
from fastapi import Depends, Response
from fastapi_jwt_auth import AuthJWT


@app.get("/subjects/{subject_id}/assignments")
async def get_subject_assignments(
    subject_id, response: Response, Auth: AuthJWT = Depends()
):
    Auth.jwt_required()

    assignments = (
        db.query(Assignments).filter(Assignments.subject_id == subject_id).all()
    )

    return assignments


@app.get("/assignments/{assignment_id}")
async def get_assignment_details(
    assignment_id, response: Response, Auth: AuthJWT = Depends()
):
    Auth.jwt_required()

    assignment = db.query(Assignments).filter(Assignments.id == assignment_id).first()

    return assignment

