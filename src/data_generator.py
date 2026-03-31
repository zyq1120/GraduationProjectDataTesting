"""
数据生成器
Data Generator - generates realistic test data for graduation project
"""

import random
from datetime import datetime, timedelta
from faker import Faker
from src.models import Student, Course, Score, get_session

fake_zh = Faker("zh_CN")
fake_en = Faker("en_US")

MAJORS = [
    "计算机科学与技术",
    "软件工程",
    "信息管理与信息系统",
    "数据科学与大数据技术",
    "人工智能",
    "网络工程",
    "电子信息工程",
    "通信工程",
    "数学与应用数学",
    "统计学",
]

DEPARTMENTS = [
    "计算机学院",
    "信息工程学院",
    "数学学院",
    "电子工程学院",
    "管理学院",
]

COURSES = [
    ("CS101", "计算机导论", 3.0, "计算机学院"),
    ("CS201", "数据结构", 4.0, "计算机学院"),
    ("CS202", "算法设计与分析", 4.0, "计算机学院"),
    ("CS301", "数据库原理", 3.5, "计算机学院"),
    ("CS302", "操作系统", 4.0, "计算机学院"),
    ("CS303", "计算机网络", 3.5, "计算机学院"),
    ("CS401", "软件工程", 3.0, "计算机学院"),
    ("CS402", "机器学习", 4.0, "计算机学院"),
    ("MATH101", "高等数学", 5.0, "数学学院"),
    ("MATH201", "线性代数", 4.0, "数学学院"),
    ("MATH301", "概率论与数理统计", 4.0, "数学学院"),
    ("EE101", "电路基础", 4.0, "电子工程学院"),
    ("IS201", "信息系统分析与设计", 3.0, "信息工程学院"),
    ("DS301", "大数据技术", 4.0, "计算机学院"),
    ("AI401", "深度学习", 4.0, "计算机学院"),
]

SEMESTERS = [
    "2021-2022-1",
    "2021-2022-2",
    "2022-2023-1",
    "2022-2023-2",
    "2023-2024-1",
    "2023-2024-2",
]


def generate_student_id(grade: int, index: int) -> str:
    """生成学号 / Generate student ID"""
    return f"{grade}{str(index).zfill(4)}"


def generate_students(count: int = 100) -> list[dict]:
    """
    生成学生数据 / Generate student data

    Args:
        count: Number of students to generate

    Returns:
        List of student dictionaries
    """
    students = []
    emails_used = set()

    for i in range(1, count + 1):
        grade = random.choice([2020, 2021, 2022, 2023])
        name = fake_zh.name()
        gender = random.choice(["男", "女"])
        age = 2024 - grade + random.choice([17, 18, 19])

        # ensure unique email
        email = fake_en.email()
        while email in emails_used:
            email = fake_en.email()
        emails_used.add(email)

        student = {
            "student_id": generate_student_id(grade, i),
            "name": name,
            "gender": gender,
            "age": age,
            "major": random.choice(MAJORS),
            "grade": grade,
            "email": email,
            "phone": fake_zh.phone_number(),
            "is_active": random.random() > 0.05,
        }
        students.append(student)

    return students


def generate_courses() -> list[dict]:
    """
    生成课程数据 / Generate course data

    Returns:
        List of course dictionaries
    """
    courses = []
    teachers = [fake_zh.name() for _ in range(20)]

    for code, name, credits, dept in COURSES:
        course = {
            "course_code": code,
            "course_name": name,
            "credits": credits,
            "department": dept,
            "teacher": random.choice(teachers),
            "description": f"{name}课程，学分{credits}",
            "max_students": random.choice([50, 80, 100, 120, 150]),
        }
        courses.append(course)

    return courses


def generate_scores(student_ids: list[int], course_ids: list[int], count: int = 500) -> list[dict]:
    """
    生成成绩数据 / Generate score data

    Args:
        student_ids: List of student database IDs
        course_ids: List of course database IDs
        count: Number of scores to generate

    Returns:
        List of score dictionaries
    """
    scores = []
    combinations_used = set()

    attempts = 0
    max_attempts = count * 10

    while len(scores) < count and attempts < max_attempts:
        attempts += 1
        student_id = random.choice(student_ids)
        course_id = random.choice(course_ids)
        semester = random.choice(SEMESTERS)
        key = (student_id, course_id, semester)

        if key in combinations_used:
            continue

        combinations_used.add(key)

        # generate realistic score distribution (normal distribution centered at 72)
        raw_score = random.gauss(72, 15)
        score = max(0.0, min(100.0, round(raw_score, 1)))

        exam_date = datetime(2021, 9, 1) + timedelta(
            days=random.randint(0, 365 * 3)
        )

        scores.append({
            "student_id": student_id,
            "course_id": course_id,
            "score": score,
            "semester": semester,
            "exam_date": exam_date,
        })

    return scores


def seed_database(engine, student_count: int = 100, score_count: int = 500) -> dict:
    """
    填充数据库测试数据 / Seed database with test data

    Args:
        engine: SQLAlchemy engine
        student_count: Number of students to create
        score_count: Number of scores to create

    Returns:
        Dictionary with counts of created records
    """
    session = get_session(engine)

    try:
        # create students
        student_dicts = generate_students(student_count)
        student_objects = [Student(**s) for s in student_dicts]
        session.add_all(student_objects)
        session.flush()

        student_ids = [s.id for s in student_objects]

        # create courses
        course_dicts = generate_courses()
        course_objects = [Course(**c) for c in course_dicts]
        session.add_all(course_objects)
        session.flush()

        course_ids = [c.id for c in course_objects]

        # create scores
        score_dicts = generate_scores(student_ids, course_ids, score_count)
        score_objects = [Score(**s) for s in score_dicts]
        session.add_all(score_objects)

        session.commit()

        return {
            "students": len(student_objects),
            "courses": len(course_objects),
            "scores": len(score_objects),
        }

    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
