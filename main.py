from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database import AsyncSessionLocal, engine, Base
import crud, schemas

app = FastAPI()


# Создаем таблицы при старте (опционально)
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Зависимость для получения сессии БД
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as db:
        yield db


# Эндпоинты для пользователей
@app.post("/users/", response_model=schemas.User)
async def create_new_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user_by_login(db, login=user.login)
    if db_user:
        raise HTTPException(status_code=400, detail="User with this login already exists")
    return await crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    users = await crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.delete("/users/{user_id}")
async def remove_user(user_id: int, db: AsyncSession = Depends(get_db)):
    success = await crud.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}


# Эндпоинты для студентов
@app.post("/students/", response_model=schemas.Student)
async def create_new_student(student: schemas.StudentCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_student(db=db, student=student)


@app.get("/students/", response_model=list[schemas.Student])
async def read_students(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.get_students(db, skip=skip, limit=limit)


@app.get("/students/{student_id}", response_model=schemas.Student)
async def read_student(student_id: int, db: AsyncSession = Depends(get_db)):
    db_student = await crud.get_student(db, student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student


@app.delete("/students/{student_id}")
async def remove_student(student_id: int, db: AsyncSession = Depends(get_db)):
    success = await crud.delete_student(db, student_id)
    if not success:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"detail": "Student deleted successfully"}


# Эндпоинты для учителей
@app.post("/teachers/", response_model=schemas.Teacher)
async def create_new_teacher(teacher: schemas.TeacherCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_teacher(db=db, teacher=teacher)


@app.get("/teachers/", response_model=list[schemas.Teacher])
async def read_teachers(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.get_teachers(db, skip=skip, limit=limit)


@app.get("/teachers/{teacher_id}", response_model=schemas.Teacher)
async def read_teacher(teacher_id: int, db: AsyncSession = Depends(get_db)):
    db_teacher = await crud.get_teacher(db, teacher_id)
    if db_teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return db_teacher


@app.delete("/teachers/{teacher_id}")
async def remove_teacher(teacher_id: int, db: AsyncSession = Depends(get_db)):
    success = await crud.delete_teacher(db, teacher_id)
    if not success:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return {"detail": "Teacher deleted successfully"}
