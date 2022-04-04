import os
import pickle

from app import app
from app.database import db
from app.database.models.marks import Marks
from app.database.models.assignments import Assignments
from starlette import status
from starlette.requests import Request
from starlette.responses import Response


@app.get("/predict-score")
async def predict_score(student_id: int, subject_id: int, resp: Response):
    clf = pickle.load(open("model.bin", "rb"))

    if not hasattr(clf, "predict"):
        resp.status_code = status.HTTP_412_PRECONDITION_FAILED
        return {"result": "Could not load model for prediction"}

    marks = (
      db.query(Marks.marks, Assignments.max_marks)
          .filter(Assignments.subject_id == subject_id)
          .filter(Marks.student_id == student_id)
          .filter(Marks.assignment_id == Assignments.id)
          .all()
    )

    score = total = 0
    for mark in marks:
        score += mark[0]
        total += mark[1]

    cpi = round((score / total) * 10, 2)

    predicted_cpi = clf.predict([[cpi]])

    return {
      "cpi": cpi,
      "predicted-cpi": predicted_cpi
    }

