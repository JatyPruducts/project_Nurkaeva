from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Users, StudentsDB, TeachersDB
from schemas import User, UserCreate, StudentCreate, TeacherCreate


# CRUD для пользователей
async def create_user(db: AsyncSession, user: UserCreate):
    db_user = Users(
        name=user.name,
        surname=user.surname,
        role=user.role,
        login=user.login,
        password=user.password
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(Users).where(Users.id == user_id))
    return result.scalar_one_or_none()


async def get_user_by_login(db: AsyncSession, login: str):
    result = await db.execute(select(Users).where(Users.login == login))
    return result.scalar_one_or_none()


async def check_user(db: AsyncSession, login: str, password: str):
    result = await db.execute(select(Users).where(Users.login == login).where(Users.password == password))
    return result.scalars().first()


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Users).offset(skip).limit(limit))
    return result.scalars().all()


async def delete_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(Users).where(Users.id == user_id))
    user = result.scalar_one_or_none()
    if user:
        await db.delete(user)
        await db.commit()
        return True
    return False


# CRUD для студентов
async def create_student(db: AsyncSession, student: StudentCreate):
    db_student = StudentsDB(
        user_id=student.user_id,
        teacher_login=student.teacher_login,
        ready_lessons=student.ready_lessons
    )
    db.add(db_student)
    await db.commit()
    await db.refresh(db_student)
    return db_student


async def get_student(db: AsyncSession, user_id: int):
    result = await db.execute(select(StudentsDB).where(StudentsDB.user_id == user_id))
    return result.scalar_one_or_none()


async def get_students(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(StudentsDB).offset(skip).limit(limit))
    return result.scalars().all()


async def delete_student(db: AsyncSession, user_id: int):
    result = await db.execute(select(StudentsDB).where(StudentsDB.user_id == user_id))
    student = result.scalar_one_or_none()
    if student:
        await db.delete(student)
        await db.commit()
        return True
    return False


# CRUD для учителей
async def create_teacher(db: AsyncSession, teacher: TeacherCreate):
    db_teacher = TeachersDB(
        user_id=teacher.user_id,
        teacher_login=teacher.teacher_login)
    db.add(db_teacher)
    await db.commit()
    await db.refresh(db_teacher)
    return db_teacher


async def check_teacher(db: AsyncSession, teacher_login: str):
    result = await db.execute(select(TeachersDB).where(TeachersDB.teacher_login == teacher_login))
    return result.scalars().first()


async def get_students_by_teacher_login(db: AsyncSession, teacher_login: str):
    # Запрос на получение пользователей (учеников) напрямую с использованием подзапроса
    print('Вошли')
    stmt = (
        select(Users)
        .join(StudentsDB)
        .where(StudentsDB.teacher_login == teacher_login)
    )
    print(stmt)
    result = await db.execute(stmt)
    users = result.scalars().all()

    return [User(id=user.id, name=user.name, surname=user.surname, role=user.role, login=user.login) for user in users]


async def get_teacher(db: AsyncSession, user_id: int):
    result = await db.execute(select(TeachersDB).where(TeachersDB.user_id == user_id))
    return result.scalar_one_or_none()


async def get_teachers(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(TeachersDB).offset(skip).limit(limit))
    return result.scalars().all()


async def delete_teacher(db: AsyncSession, user_id: int):
    result = await db.execute(select(TeachersDB).where(TeachersDB.user_id == user_id))
    teacher = result.scalar_one_or_none()
    if teacher:
        await db.delete(teacher)
        await db.commit()
        return True
    return False
