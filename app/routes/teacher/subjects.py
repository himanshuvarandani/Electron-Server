from app import app
from app.database import db
from app.database.models.subjects import Subjects
from app.database.models.subject_class_map import SubjectClassMap
from app.database.models.teacher_subject_map import TeacherSubjectMap
from fastapi import Response, status


@app.get("/teachers/{teacher_id}/list-class-subjects")
async def teacher_class_subjects(teacher_id, class_id: int, response: Response):
    subjects = (
        db.query(Subjects)
        .join(TeacherSubjectMap, TeacherSubjectMap.teacher_id == teacher_id)
        .join(SubjectClassMap, SubjectClassMap.class_id == class_id)
        .filter(TeacherSubjectMap.subject_id == SubjectClassMap.subject_id)
        .filter(Subjects.id == TeacherSubjectMap.subject_id)
        .all()
    )

    if not subjects:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"result": "fail", "reason": "No subjects found"}

    return subjects
