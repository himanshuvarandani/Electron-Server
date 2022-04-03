import os
import pickle

from app import app
from app.database import db
from app.database.models.students import Students
from starlette import status
from starlette.requests import Request
from starlette.responses import Response


@app.get("/predict-score")
async def predict_score(student_id: int, subject_id: int, resp: Response):
    clf = pickle.load(open("model.bin", "wb"))

    if not hasattr(clf, "predict"):
        resp.status_code = status.HTTP_412_PRECONDITION_FAILED
        return {"result": "Could not load model for prediction"}

    # TODO: Fetch marks from database
    # marks = db.query(...)

    student = db.query(student).filter(Students == student_id).first()
    clf.predict([marks])
