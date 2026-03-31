"""
数据模型定义
Data Models Definition
"""

from datetime import datetime, timezone
from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey, create_engine
)
from sqlalchemy.orm import relationship, DeclarativeBase, Session
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class Student(Base):
    """学生信息表 / Student information table"""
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String(20), unique=True, nullable=False, comment="学号")
    name = Column(String(50), nullable=False, comment="姓名")
    gender = Column(String(10), nullable=False, comment="性别")
    age = Column(Integer, nullable=False, comment="年龄")
    major = Column(String(100), nullable=False, comment="专业")
    grade = Column(Integer, nullable=False, comment="年级")
    email = Column(String(100), unique=True, nullable=False, comment="邮箱")
    phone = Column(String(20), comment="手机号")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), comment="创建时间")
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), comment="更新时间")
    is_active = Column(Boolean, default=True, comment="是否在校")

    scores = relationship("Score", back_populates="student", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Student(id={self.id}, student_id={self.student_id}, name={self.name})>"

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "name": self.name,
            "gender": self.gender,
            "age": self.age,
            "major": self.major,
            "grade": self.grade,
            "email": self.email,
            "phone": self.phone,
            "is_active": self.is_active,
        }


class Course(Base):
    """课程信息表 / Course information table"""
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_code = Column(String(20), unique=True, nullable=False, comment="课程代码")
    course_name = Column(String(100), nullable=False, comment="课程名称")
    credits = Column(Float, nullable=False, comment="学分")
    department = Column(String(100), nullable=False, comment="开课学院")
    teacher = Column(String(50), nullable=False, comment="授课教师")
    description = Column(Text, comment="课程描述")
    max_students = Column(Integer, default=100, comment="最大选课人数")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), comment="创建时间")

    scores = relationship("Score", back_populates="course", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Course(id={self.id}, course_code={self.course_code}, course_name={self.course_name})>"

    def to_dict(self):
        return {
            "id": self.id,
            "course_code": self.course_code,
            "course_name": self.course_name,
            "credits": self.credits,
            "department": self.department,
            "teacher": self.teacher,
            "max_students": self.max_students,
        }


class Score(Base):
    """成绩表 / Score table"""
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, comment="学生ID")
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, comment="课程ID")
    score = Column(Float, nullable=False, comment="成绩")
    semester = Column(String(20), nullable=False, comment="学期")
    exam_date = Column(DateTime, comment="考试日期")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), comment="创建时间")

    student = relationship("Student", back_populates="scores")
    course = relationship("Course", back_populates="scores")

    def __repr__(self):
        return f"<Score(student_id={self.student_id}, course_id={self.course_id}, score={self.score})>"

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "course_id": self.course_id,
            "score": self.score,
            "semester": self.semester,
        }


def create_db_engine(db_url: str = "sqlite:///:memory:"):
    """创建数据库引擎 / Create database engine"""
    engine = create_engine(db_url, echo=False)
    Base.metadata.create_all(engine)
    return engine


def get_session(engine) -> Session:
    """获取数据库会话 / Get database session"""
    return Session(engine)
