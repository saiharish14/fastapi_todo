# from fastapi import FastAPI, Depends, HTTPException, Request, status
# from fastapi.responses import JSONResponse
# from pydantic import BaseModel, ValidationError
#
# app = FastAPI()
# students = []
#
# class Student(BaseModel):
#     name: str
#     age: int
#     grade: str
#
# # Global exception handler for validation errors
# @app.exception_handler(ValidationError)
# async def validation_exception_handler(request: Request, exc: ValidationError):
#     return JSONResponse(
#         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#         content={"detail": exc.errors(), "body": exc.body},
#     )
#
# # Global handler for general exceptions
# @app.exception_handler(Exception)
# async def general_exception_handler(request: Request, exc: Exception):
#     return JSONResponse(
#         status_code=500,
#         content={"message": "Internal Server Error", "error": str(exc)},
#     )
#
# @app.get("/")
# def read_root():
#     return {"message": "My self Harish!"}
#
# @app.get("/students")
# def get_students():
#     return students
#
# @app.head("/students")
# def head_students():
#     return {"X-Total-Students": len(students)}
#
# @app.options("/students")
# def option_students():
#     return {
#         "allowed_methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"],
#     }
#
# @app.post("/students")
# def create_student(student: Student):
#     try:
#         students.append(student.dict())
#         return {"message": "Student added", "data": student}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
#
# @app.get("/students/{student_id}")
# def get_student(student_id: int):
#     if 0 <= student_id < len(students):
#         return students[student_id]
#     raise HTTPException(status_code=404, detail="Student not found")
#
# @app.put("/students/{student_id}")
# def update_student(student_id: int, student: Student):
#     if 0 <= student_id < len(students):
#         students[student_id] = student.dict()
#         return {"message": "Student updated", "data": student}
#     raise HTTPException(status_code=404, detail="Student not found")
#
# @app.patch("/students/{student_id}")
# def partial_update_student(student_id: int, student: Student):
#     if 0 <= student_id < len(students):
#         current_data = students[student_id]
#         update_data = student.dict(exclude_unset=True)
#         current_data.update(update_data)
#         students[student_id] = current_data
#         return {"message": "Student partially updated", "data": current_data}
#     raise HTTPException(status_code=404, detail="Student not found")
#
# @app.delete("/students/{student_id}")
# def delete_student(student_id: int):
#     if 0 <= student_id < len(students):
#         removed = students.pop(student_id)
#         return {"message": "Student removed", "data": removed}
#     raise HTTPException(status_code=404, detail="Student not found")
#
# @app.get("/search")
# def search_students(name: str = None):
#     try:
#         if name:
#             results = [s for s in students if s["name"].lower() == name.lower()]
#             return {"results": results}
#         return {"results": "No name provided"}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
#
# def common_dependency():
#     return {"note": "common dependency injected"}
#
# @app.get("/check")
# def check(dep=Depends(common_dependency)):
#     return dep




from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# In-memory list to simulate a database
students = []

# Data model for a student
class Student(BaseModel):
    name: str
    age: int
    grade: str

# Data model for partial update
class StudentUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    grade: Optional[str] = None

def common_dependency():
    return {"note": "common dependency injected"}

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}

@app.get("/students")
def get_students():
    return students

@app.head("/students")
def head_students():
    return {"X-Total-Students": len(students)}

@app.options("/students")
def option_students():
    return {
        "allowed_methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"],
    }

@app.post("/students")
def create_student(student: Student):
    students.append(student.dict())
    return {"message": "Student added", "data": student}

@app.get("/students/{student_id}")
def get_student(student_id: int):
    if 0 <= student_id < len(students):
        return students[student_id]
    raise HTTPException(status_code=404, detail="Student not found")

@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    if 0 <= student_id < len(students):
        students[student_id] = student.dict()
        return {"message": "Student updated", "data": student}
    raise HTTPException(status_code=404, detail="Student not found")

@app.patch("/students/{student_id}")
def partial_update_student(student_id: int, student: StudentUpdate):
    if 0 <= student_id < len(students):
        current_data = students[student_id]
        update_data = student.dict(exclude_unset=True)
        current_data.update(update_data)
        students[student_id] = current_data
        return {"message": "Student partially updated", "data": current_data}
    raise HTTPException(status_code=404, detail="Student not found")

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    if 0 <= student_id < len(students):
        removed = students.pop(student_id)
        return {"message": "Student deleted", "data": removed}
    raise HTTPException(status_code=404, detail="Student not found")

@app.get("/search")
def search_students(name: str = None):
    if name:
        results = [s for s in students if s["name"].lower() == name.lower()]
        return {"results": results}
    return {"message": "No name provided"}

@app.get("/check")
def check(dep=Depends(common_dependency)):
    return dep

