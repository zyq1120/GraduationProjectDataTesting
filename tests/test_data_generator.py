"""
数据生成器测试
Tests for data generator functions
"""

import pytest
from src.data_generator import (
    generate_students,
    generate_courses,
    generate_scores,
    seed_database,
    MAJORS,
    COURSES,
)
from src.models import Student, Course, Score, create_db_engine, get_session


class TestGenerateStudents:
    """学生数据生成器测试 / Student data generator tests"""

    def test_generates_correct_count(self):
        students = generate_students(10)
        assert len(students) == 10

    def test_generates_default_100(self):
        students = generate_students()
        assert len(students) == 100

    def test_student_has_required_fields(self):
        students = generate_students(1)
        s = students[0]
        required = ["student_id", "name", "gender", "age", "major", "grade", "email"]
        for field in required:
            assert field in s, f"Missing field: {field}"

    def test_all_emails_unique(self):
        students = generate_students(50)
        emails = [s["email"] for s in students]
        assert len(emails) == len(set(emails))

    def test_all_student_ids_unique(self):
        students = generate_students(50)
        ids = [s["student_id"] for s in students]
        assert len(ids) == len(set(ids))

    def test_valid_gender_values(self):
        students = generate_students(20)
        for s in students:
            assert s["gender"] in ("男", "女")

    def test_valid_major_values(self):
        students = generate_students(20)
        for s in students:
            assert s["major"] in MAJORS

    def test_valid_grade_values(self):
        students = generate_students(20)
        for s in students:
            assert 2000 <= s["grade"] <= 2030

    def test_age_in_reasonable_range(self):
        students = generate_students(50)
        for s in students:
            assert 15 <= s["age"] <= 40

    def test_is_active_is_boolean(self):
        students = generate_students(20)
        for s in students:
            assert isinstance(s["is_active"], bool)


class TestGenerateCourses:
    """课程数据生成器测试 / Course data generator tests"""

    def test_generates_all_predefined_courses(self):
        courses = generate_courses()
        assert len(courses) == len(COURSES)

    def test_course_has_required_fields(self):
        courses = generate_courses()
        required = ["course_code", "course_name", "credits", "department", "teacher"]
        for course in courses:
            for field in required:
                assert field in course, f"Missing field: {field}"

    def test_all_course_codes_unique(self):
        courses = generate_courses()
        codes = [c["course_code"] for c in courses]
        assert len(codes) == len(set(codes))

    def test_credits_positive(self):
        courses = generate_courses()
        for c in courses:
            assert c["credits"] > 0

    def test_max_students_in_range(self):
        courses = generate_courses()
        for c in courses:
            assert 1 <= c["max_students"] <= 500


class TestGenerateScores:
    """成绩数据生成器测试 / Score data generator tests"""

    def test_generates_up_to_requested_count(self):
        student_ids = list(range(1, 21))
        course_ids = list(range(1, 16))
        scores = generate_scores(student_ids, course_ids, count=100)
        assert 0 < len(scores) <= 100

    def test_score_has_required_fields(self):
        student_ids = list(range(1, 11))
        course_ids = list(range(1, 6))
        scores = generate_scores(student_ids, course_ids, count=10)
        required = ["student_id", "course_id", "score", "semester"]
        for s in scores:
            for field in required:
                assert field in s

    def test_scores_in_valid_range(self):
        student_ids = list(range(1, 21))
        course_ids = list(range(1, 11))
        scores = generate_scores(student_ids, course_ids, count=100)
        for s in scores:
            assert 0 <= s["score"] <= 100

    def test_no_duplicate_student_course_semester(self):
        student_ids = list(range(1, 21))
        course_ids = list(range(1, 11))
        scores = generate_scores(student_ids, course_ids, count=50)
        combinations = [(s["student_id"], s["course_id"], s["semester"]) for s in scores]
        assert len(combinations) == len(set(combinations))


class TestSeedDatabase:
    """数据库填充测试 / Database seeding tests"""

    def test_seed_returns_counts(self):
        engine = create_db_engine("sqlite:///:memory:")
        result = seed_database(engine, student_count=10, score_count=30)
        assert "students" in result
        assert "courses" in result
        assert "scores" in result

    def test_seed_creates_correct_student_count(self):
        engine = create_db_engine("sqlite:///:memory:")
        result = seed_database(engine, student_count=20, score_count=50)
        assert result["students"] == 20

    def test_seed_creates_courses(self):
        engine = create_db_engine("sqlite:///:memory:")
        result = seed_database(engine, student_count=5, score_count=10)
        assert result["courses"] == len(COURSES)

    def test_seed_creates_scores_in_db(self):
        engine = create_db_engine("sqlite:///:memory:")
        seed_database(engine, student_count=20, score_count=50)
        session = get_session(engine)
        count = session.query(Score).count()
        session.close()
        assert count > 0

    def test_seed_students_retrievable(self):
        engine = create_db_engine("sqlite:///:memory:")
        seed_database(engine, student_count=10, score_count=20)
        session = get_session(engine)
        students = session.query(Student).all()
        session.close()
        assert len(students) == 10

    def test_seed_scores_linked_to_students(self):
        engine = create_db_engine("sqlite:///:memory:")
        seed_database(engine, student_count=10, score_count=30)
        session = get_session(engine)
        scores = session.query(Score).all()
        for score in scores:
            assert score.student is not None
            assert score.course is not None
        session.close()
