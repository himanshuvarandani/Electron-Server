from app import app
from app.database import db
from app.database.models.classes import Classes
from fastapi import Depends, Response, status
from fastapi_jwt_auth import AuthJWT


@app.get("/get-all-classes")
async def get_all_classes(response: Response, Auth: AuthJWT = Depends()):
    Auth.jwt_required()

    classes = db.query(Classes).all()

    if not classes:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"result": "fail", "reason": "No classes found"}

    return classes
