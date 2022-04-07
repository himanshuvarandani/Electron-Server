from app import app
from app.database import db
from app.database.models.assignments import Assignments
from app.database.models.student_subject_map import StudentSubjectMap
from app.database.models.submissions import Submissions
from sqlalchemy.sql import func
from starlette.responses import Response


@app.get("/students/{student_id}/stats/compare-score")
async def compare_score(student_id: int, assignment_id: int, resp: Response):
    marks = (
        db.query(Submissions.subject_id, Submissions.marks)
            .filter(StudentSubjectMap.student_id == student_id)
            .filter(Submissions.student_id == student_id)
            .filter(Submissions.assignment_id == assignment_id)
            .filter(Submissions.subject_id == StudentSubjectMap.subject_id)
            .all()
    )

    avg_marks = (
        db.query(Submissions.subject_id, func.avg(Submissions.marks).label('avg_marks'))
            .filter(Submissions.assignment_id == assignment_id)
            .group_by(Submissions.subject_id)
            .all()
    )

    result = []
    for i in marks:
        for j in avg_marks:
            if i.subject_id == j.subject_id:
                result.append({
                    subject_id: i.subject_id,
                    marks: i.marks,
                    avg_marks: j.avg_marks
                })

    return result
