"""
数据库CRUD操作测试
Tests for database CRUD operations
"""

import pytest
from sqlalchemy.exc import IntegrityError
from src.models import Student, Course, Score, get_session


# ---------------------------------------------------------------------------
# Student CRUD tests
# ---------------------------------------------------------------------------

class TestStudentCRUD:
    """学生CRUD操作测试 / Student CRUD operation tests"""

    def test_create_student(self, session):
        student = Student(
            student_id="20210001",
            name="张三",
            gender="男",
            age=20,
            major="计算机科学与技术",
            grade=2021,
            email="zhangsan@test.com",
        )
        session.add(student)
        session.flush()
        assert student.id is not None
        assert student.is_active is True

    def test_read_student(self, session):
        student = Student(
            student_id="20210002",
            name="李四",
            gender="女",
            age=21,
            major="软件工程",
            grade=2021,
            email="lisi@test.com",
        )
        session.add(student)
        session.flush()

        found = session.get(Student, student.id)
        assert found is not None
        assert found.name == "李四"
        assert found.major == "软件工程"

    def test_update_student(self, session):
        student = Student(
            student_id="20210003",
            name="王五",
            gender="男",
            age=22,
            major="数据科学与大数据技术",
            grade=2021,
            email="wangwu@test.com",
        )
        session.add(student)
        session.flush()

        student.age = 23
        student.email = "wangwu_updated@test.com"
        session.flush()

        updated = session.get(Student, student.id)
        assert updated.age == 23
        assert updated.email == "wangwu_updated@test.com"

    def test_delete_student(self, session):
        student = Student(
            student_id="20210004",
            name="赵六",
            gender="女",
            age=20,
            major="人工智能",
            grade=2021,
            email="zhaoliu@test.com",
        )
        session.add(student)
        session.flush()
        student_id = student.id

        session.delete(student)
        session.flush()

        assert session.get(Student, student_id) is None

    def test_student_unique_student_id(self, session):
        s1 = Student(
            student_id="20210005",
            name="A",
            gender="男",
            age=20,
            major="计算机科学与技术",
            grade=2021,
            email="a@test.com",
        )
        s2 = Student(
            student_id="20210005",  # duplicate
            name="B",
            gender="男",
            age=20,
            major="计算机科学与技术",
            grade=2021,
            email="b@test.com",
        )
        session.add(s1)
        session.flush()

        session.add(s2)
        with pytest.raises(IntegrityError):
            session.flush()
        session.rollback()

    def test_student_unique_email(self, session):
        s1 = Student(
            student_id="20210006",
            name="C",
            gender="男",
            age=20,
            major="计算机科学与技术",
            grade=2021,
            email="duplicate@test.com",
        )
        s2 = Student(
            student_id="20210007",
            name="D",
            gender="女",
            age=21,
            major="软件工程",
            grade=2021,
            email="duplicate@test.com",  # duplicate email
        )
        session.add(s1)
        session.flush()

        session.add(s2)
        with pytest.raises(IntegrityError):
            session.flush()
        session.rollback()

    def test_student_to_dict(self, session):
        student = Student(
            student_id="20210008",
            name="孙七",
            gender="男",
            age=20,
            major="网络工程",
            grade=2021,
            email="sunqi@test.com",
        )
        session.add(student)
        session.flush()

        d = student.to_dict()
        assert d["name"] == "孙七"
        assert d["student_id"] == "20210008"
        assert "email" in d


# ---------------------------------------------------------------------------
# Course CRUD tests
# ---------------------------------------------------------------------------

class TestCourseCRUD:
    """课程CRUD操作测试 / Course CRUD operation tests"""

    def test_create_course(self, session):
        course = Course(
            course_code="TEST001",
            course_name="测试课程",
            credits=3.0,
            department="计算机学院",
            teacher="测试老师",
        )
        session.add(course)
        session.flush()
        assert course.id is not None
        assert course.max_students == 100  # default value

    def test_read_course(self, session):
        course = Course(
            course_code="TEST002",
            course_name="测试课程2",
            credits=4.0,
            department="数学学院",
            teacher="数学老师",
        )
        session.add(course)
        session.flush()

        found = session.get(Course, course.id)
        assert found.course_name == "测试课程2"
        assert found.credits == 4.0

    def test_update_course(self, session):
        course = Course(
            course_code="TEST003",
            course_name="原始课程名",
            credits=2.0,
            department="电子工程学院",
            teacher="电子老师",
        )
        session.add(course)
        session.flush()

        course.course_name = "更新后的课程名"
        course.credits = 3.0
        session.flush()

        updated = session.get(Course, course.id)
        assert updated.course_name == "更新后的课程名"
        assert updated.credits == 3.0

    def test_delete_course(self, session):
        course = Course(
            course_code="TEST004",
            course_name="待删除课程",
            credits=1.0,
            department="管理学院",
            teacher="管理老师",
        )
        session.add(course)
        session.flush()
        cid = course.id

        session.delete(course)
        session.flush()

        assert session.get(Course, cid) is None

    def test_course_unique_code(self, session):
        c1 = Course(
            course_code="DUPCODE",
            course_name="课程1",
            credits=3.0,
            department="计算机学院",
            teacher="老师1",
        )
        c2 = Course(
            course_code="DUPCODE",  # duplicate
            course_name="课程2",
            credits=3.0,
            department="计算机学院",
            teacher="老师2",
        )
        session.add(c1)
        session.flush()
        session.add(c2)
        with pytest.raises(IntegrityError):
            session.flush()
        session.rollback()


# ---------------------------------------------------------------------------
# Score CRUD tests
# ---------------------------------------------------------------------------

class TestScoreCRUD:
    """成绩CRUD操作测试 / Score CRUD operation tests"""

    def _create_student_and_course(self, session, suffix=""):
        student = Student(
            student_id=f"2021900{suffix}",
            name=f"测试生{suffix}",
            gender="男",
            age=20,
            major="计算机科学与技术",
            grade=2021,
            email=f"teststu{suffix}@test.com",
        )
        course = Course(
            course_code=f"SCRTEST{suffix}",
            course_name=f"成绩测试课{suffix}",
            credits=3.0,
            department="计算机学院",
            teacher="成绩老师",
        )
        session.add_all([student, course])
        session.flush()
        return student, course

    def test_create_score(self, session):
        student, course = self._create_student_and_course(session, "A")
        score = Score(
            student_id=student.id,
            course_id=course.id,
            score=88.5,
            semester="2023-2024-1",
        )
        session.add(score)
        session.flush()
        assert score.id is not None

    def test_read_score(self, session):
        student, course = self._create_student_and_course(session, "B")
        score = Score(
            student_id=student.id,
            course_id=course.id,
            score=75.0,
            semester="2023-2024-2",
        )
        session.add(score)
        session.flush()

        found = session.get(Score, score.id)
        assert found.score == 75.0
        assert found.semester == "2023-2024-2"

    def test_score_cascades_with_student_delete(self, session):
        student, course = self._create_student_and_course(session, "C")
        score = Score(
            student_id=student.id,
            course_id=course.id,
            score=60.0,
            semester="2022-2023-1",
        )
        session.add(score)
        session.flush()
        score_id = score.id

        session.delete(student)
        session.flush()

        assert session.get(Score, score_id) is None

    def test_score_relationship_to_student(self, session):
        student, course = self._create_student_and_course(session, "D")
        score = Score(
            student_id=student.id,
            course_id=course.id,
            score=95.0,
            semester="2021-2022-1",
        )
        session.add(score)
        session.flush()

        assert score.student.name == f"测试生D"
        assert score.course.course_name == "成绩测试课D"

    def test_update_score(self, session):
        student, course = self._create_student_and_course(session, "E")
        score = Score(
            student_id=student.id,
            course_id=course.id,
            score=50.0,
            semester="2021-2022-2",
        )
        session.add(score)
        session.flush()

        score.score = 70.0
        session.flush()

        updated = session.get(Score, score.id)
        assert updated.score == 70.0
