"""
数据验证测试
Tests for data validation logic
"""

import pytest
from src.validators import (
    validate_student,
    validate_course,
    validate_score,
    validate_dataset,
    ValidationResult,
)


# ---------------------------------------------------------------------------
# Student validation tests
# ---------------------------------------------------------------------------

class TestStudentValidation:
    """学生数据验证测试 / Student data validation tests"""

    def _valid_student(self, **overrides) -> dict:
        base = {
            "student_id": "20210001",
            "name": "张三",
            "gender": "男",
            "age": 20,
            "major": "计算机科学与技术",
            "grade": 2021,
            "email": "zhangsan@example.com",
            "phone": "13800138000",
        }
        base.update(overrides)
        return base

    def test_valid_student_passes(self):
        result = validate_student(self._valid_student())
        assert result.is_valid

    def test_missing_student_id(self):
        result = validate_student(self._valid_student(student_id=""))
        assert not result.is_valid
        assert any(e.field == "student_id" for e in result.errors)

    def test_invalid_student_id_format(self):
        result = validate_student(self._valid_student(student_id="ABC"))
        assert not result.is_valid
        assert any(e.field == "student_id" for e in result.errors)

    def test_missing_name(self):
        result = validate_student(self._valid_student(name=""))
        assert not result.is_valid
        assert any(e.field == "name" for e in result.errors)

    def test_name_too_short(self):
        result = validate_student(self._valid_student(name="A"))
        assert not result.is_valid

    def test_name_too_long(self):
        result = validate_student(self._valid_student(name="A" * 51))
        assert not result.is_valid

    def test_invalid_gender(self):
        result = validate_student(self._valid_student(gender="other"))
        assert not result.is_valid
        assert any(e.field == "gender" for e in result.errors)

    def test_valid_genders(self):
        assert validate_student(self._valid_student(gender="男")).is_valid
        assert validate_student(self._valid_student(gender="女")).is_valid

    def test_age_too_young(self):
        result = validate_student(self._valid_student(age=14))
        assert not result.is_valid
        assert any(e.field == "age" for e in result.errors)

    def test_age_too_old(self):
        result = validate_student(self._valid_student(age=61))
        assert not result.is_valid

    def test_age_boundary_valid(self):
        assert validate_student(self._valid_student(age=15)).is_valid
        assert validate_student(self._valid_student(age=60)).is_valid

    def test_invalid_email(self):
        result = validate_student(self._valid_student(email="not-an-email"))
        assert not result.is_valid
        assert any(e.field == "email" for e in result.errors)

    def test_missing_email(self):
        result = validate_student(self._valid_student(email=""))
        assert not result.is_valid

    def test_valid_email_formats(self):
        assert validate_student(self._valid_student(email="user@domain.com")).is_valid
        assert validate_student(self._valid_student(email="user.name+tag@sub.domain.org")).is_valid

    def test_invalid_grade(self):
        result = validate_student(self._valid_student(grade=1999))
        assert not result.is_valid
        assert any(e.field == "grade" for e in result.errors)

    def test_valid_grade_boundary(self):
        assert validate_student(self._valid_student(grade=2000)).is_valid
        assert validate_student(self._valid_student(grade=2030)).is_valid

    def test_phone_warning_invalid(self):
        result = validate_student(self._valid_student(phone="1234567890"))
        # phone is optional but should produce a warning
        assert len(result.warnings) > 0

    def test_phone_optional(self):
        data = self._valid_student()
        data.pop("phone", None)
        result = validate_student(data)
        assert result.is_valid


# ---------------------------------------------------------------------------
# Course validation tests
# ---------------------------------------------------------------------------

class TestCourseValidation:
    """课程数据验证测试 / Course data validation tests"""

    def _valid_course(self, **overrides) -> dict:
        base = {
            "course_code": "CS301",
            "course_name": "数据库原理",
            "credits": 3.5,
            "department": "计算机学院",
            "teacher": "李四",
            "max_students": 100,
        }
        base.update(overrides)
        return base

    def test_valid_course_passes(self):
        assert validate_course(self._valid_course()).is_valid

    def test_invalid_course_code(self):
        result = validate_course(self._valid_course(course_code="cs301"))
        assert not result.is_valid

    def test_missing_course_code(self):
        result = validate_course(self._valid_course(course_code=""))
        assert not result.is_valid

    def test_missing_course_name(self):
        result = validate_course(self._valid_course(course_name=""))
        assert not result.is_valid

    def test_credits_zero(self):
        result = validate_course(self._valid_course(credits=0))
        assert not result.is_valid

    def test_credits_negative(self):
        result = validate_course(self._valid_course(credits=-1))
        assert not result.is_valid

    def test_credits_too_high(self):
        result = validate_course(self._valid_course(credits=11))
        assert not result.is_valid

    def test_credits_boundary_valid(self):
        assert validate_course(self._valid_course(credits=0.1)).is_valid
        assert validate_course(self._valid_course(credits=0.5)).is_valid
        assert validate_course(self._valid_course(credits=10)).is_valid

    def test_missing_department(self):
        result = validate_course(self._valid_course(department=""))
        assert not result.is_valid

    def test_missing_teacher(self):
        result = validate_course(self._valid_course(teacher=""))
        assert not result.is_valid

    def test_invalid_max_students(self):
        result = validate_course(self._valid_course(max_students=0))
        assert not result.is_valid
        result = validate_course(self._valid_course(max_students=501))
        assert not result.is_valid

    def test_valid_max_students_boundary(self):
        assert validate_course(self._valid_course(max_students=1)).is_valid
        assert validate_course(self._valid_course(max_students=500)).is_valid


# ---------------------------------------------------------------------------
# Score validation tests
# ---------------------------------------------------------------------------

class TestScoreValidation:
    """成绩数据验证测试 / Score data validation tests"""

    def _valid_score(self, **overrides) -> dict:
        base = {
            "student_id": 1,
            "course_id": 1,
            "score": 85.0,
            "semester": "2023-2024-1",
        }
        base.update(overrides)
        return base

    def test_valid_score_passes(self):
        assert validate_score(self._valid_score()).is_valid

    def test_missing_student_id(self):
        result = validate_score(self._valid_score(student_id=None))
        assert not result.is_valid

    def test_missing_course_id(self):
        result = validate_score(self._valid_score(course_id=None))
        assert not result.is_valid

    def test_score_below_zero(self):
        result = validate_score(self._valid_score(score=-1))
        assert not result.is_valid

    def test_score_above_100(self):
        result = validate_score(self._valid_score(score=101))
        assert not result.is_valid

    def test_score_boundary_valid(self):
        assert validate_score(self._valid_score(score=0)).is_valid
        assert validate_score(self._valid_score(score=100)).is_valid

    def test_failing_score_warning(self):
        result = validate_score(self._valid_score(score=55))
        assert result.is_valid  # still valid, just a warning
        assert len(result.warnings) > 0

    def test_invalid_semester_format(self):
        result = validate_score(self._valid_score(semester="2023/2024-1"))
        assert not result.is_valid

    def test_missing_semester(self):
        result = validate_score(self._valid_score(semester=""))
        assert not result.is_valid

    def test_valid_semester_formats(self):
        assert validate_score(self._valid_score(semester="2021-2022-1")).is_valid
        assert validate_score(self._valid_score(semester="2023-2024-2")).is_valid

    def test_missing_score(self):
        result = validate_score(self._valid_score(score=None))
        assert not result.is_valid


# ---------------------------------------------------------------------------
# Batch dataset validation tests
# ---------------------------------------------------------------------------

class TestDatasetValidation:
    """批量数据集验证测试 / Dataset batch validation tests"""

    def test_all_valid_records(self):
        records = [
            {"student_id": 1, "course_id": 1, "score": 80, "semester": "2023-2024-1"},
            {"student_id": 2, "course_id": 2, "score": 90, "semester": "2023-2024-1"},
        ]
        summary = validate_dataset(records, validate_score)
        assert summary["total"] == 2
        assert summary["valid"] == 2
        assert summary["invalid"] == 0
        assert summary["error_rate"] == 0.0

    def test_some_invalid_records(self):
        records = [
            {"student_id": 1, "course_id": 1, "score": 80, "semester": "2023-2024-1"},
            {"student_id": None, "course_id": 1, "score": -5, "semester": "bad"},
        ]
        summary = validate_dataset(records, validate_score)
        assert summary["total"] == 2
        assert summary["invalid"] == 1
        assert summary["error_rate"] == 0.5
        assert len(summary["errors"]) > 0

    def test_empty_dataset(self):
        summary = validate_dataset([], validate_score)
        assert summary["total"] == 0
        assert summary["error_rate"] == 0
