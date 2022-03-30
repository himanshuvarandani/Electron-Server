import random
import pandas as pd

from app import app
from app.database.models.teachers import Teachers
from fastapi import Response, UploadFile, File
from pydantic import BaseModel, validator


@app.post("/admin/add_teachers")
async def add_teachers(file: bytes = File(...)):
  try:
    data = pd.read_excel(file, index_col=None)
    teachers = data.values.tolist()

    for teacherDetail in teachers:
      teacherInstance = Teachers()
      teacherInstance.name = teacherDetail[0]
      teacherInstance.email = teacherDetail[1]

      # Generate a random password
      charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
      password = ''
      for i in range(8):
        password += random.choice(charset)
      
      # Todo: Required hashing password
      teacherInstance.password_hash = password
      
      # Todo: Remove these comments:
      # try:
      #   db.add(teacherInstance)
      #   db.commit()
      # except Exception as e:
      #   print(e)

    return {"result": 'Pass'}
  except Exception as e:
    print(e)
    return {"result": e}
  