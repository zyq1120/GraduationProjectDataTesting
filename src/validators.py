"""
数据验证器
Data Validator - validates data integrity and business rules
"""

import re
from typing import Any


class ValidationError(Exception):
    """数据验证错误 / Data validation error"""

    def __init__(self, field: str, message: str, value: Any = None):
        self.field = field
        self.message = message
        self.value = value
        super().__init__(f"Validation error on field '{field}': {message} (value={value!r})")


class ValidationResult:
    """验证结果 / Validation result"""

    def __init__(self):
        self.errors: list[ValidationError] = []
        self.warnings: list[str] = []

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0

    def add_error(self, field: str, message: str, value: Any = None):
        self.errors.append(ValidationError(field, message, value))

    def add_warning(self, message: str):
        self.warnings.append(message)

    def __repr__(self):
        return (
            f"<ValidationResult(valid={self.is_valid}, "
            f"errors={len(self.errors)}, warnings={len(self.warnings)})>"
        )


EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$")
PHONE_PATTERN = re.compile(r"^1[3-9]\d{9}$")
STUDENT_ID_PATTERN = re.compile(r"^\d{8,12}$")


def validate_student(data: dict) -> ValidationResult:
    """
    验证学生数据 / Validate student data

    Args:
        data: Student data dictionary

    Returns:
        ValidationResult with any errors or warnings
    """
    result = ValidationResult()

    # student_id validation
    student_id = data.get("student_id", "")
    if not student_id:
        result.add_error("student_id", "学号不能为空", student_id)
    elif not STUDENT_ID_PATTERN.match(str(student_id)):
        result.add_error("student_id", "学号格式不正确，应为8-12位数字", student_id)

    # name validation
    name = data.get("name", "")
    if not name:
        result.add_error("name", "姓名不能为空", name)
    elif len(name) < 2 or len(name) > 50:
        result.add_error("name", "姓名长度应在2-50个字符之间", name)

    # gender validation
    gender = data.get("gender", "")
    if gender not in ("男", "女"):
        result.add_error("gender", "性别必须为'男'或'女'", gender)

    # age validation
    age = data.get("age")
    if age is None:
        result.add_error("age", "年龄不能为空", age)
    elif not isinstance(age, int) or age < 15 or age > 60:
        result.add_error("age", "年龄必须为15-60之间的整数", age)

    # major validation
    major = data.get("major", "")
    if not major:
        result.add_error("major", "专业不能为空", major)
    elif len(major) > 100:
        result.add_error("major", "专业名称不能超过100个字符", major)

    # grade validation
    grade = data.get("grade")
    if grade is None:
        result.add_error("grade", "年级不能为空", grade)
    elif not isinstance(grade, int) or grade < 2000 or grade > 2030:
        result.add_error("grade", "年级必须为2000-2030之间的整数", grade)

    # email validation
    email = data.get("email", "")
    if not email:
        result.add_error("email", "邮箱不能为空", email)
    elif not EMAIL_PATTERN.match(email):
        result.add_error("email", "邮箱格式不正确", email)

    # phone validation (optional but must be valid if provided)
    phone = data.get("phone", "")
    if phone and not PHONE_PATTERN.match(str(phone)):
        result.add_warning(f"手机号格式可能不正确: {phone}")

    return result


def validate_course(data: dict) -> ValidationResult:
    """
    验证课程数据 / Validate course data

    Args:
        data: Course data dictionary

    Returns:
        ValidationResult with any errors or warnings
    """
    result = ValidationResult()

    # course_code validation
    course_code = data.get("course_code", "")
    if not course_code:
        result.add_error("course_code", "课程代码不能为空", course_code)
    elif not re.match(r"^[A-Z]{2,6}\d{3,6}$", course_code):
        result.add_error("course_code", "课程代码格式不正确，应为2-6位大写字母加3-6位数字", course_code)

    # course_name validation
    course_name = data.get("course_name", "")
    if not course_name:
        result.add_error("course_name", "课程名称不能为空", course_name)
    elif len(course_name) > 100:
        result.add_error("course_name", "课程名称不能超过100个字符", course_name)

    # credits validation
    credits = data.get("credits")
    if credits is None:
        result.add_error("credits", "学分不能为空", credits)
    elif not isinstance(credits, (int, float)) or credits <= 0 or credits > 10:
        result.add_error("credits", "学分必须大于0且不超过10", credits)

    # department validation
    department = data.get("department", "")
    if not department:
        result.add_error("department", "开课学院不能为空", department)

    # teacher validation
    teacher = data.get("teacher", "")
    if not teacher:
        result.add_error("teacher", "授课教师不能为空", teacher)

    # max_students validation
    max_students = data.get("max_students", 100)
    if not isinstance(max_students, int) or max_students < 1 or max_students > 500:
        result.add_error("max_students", "最大选课人数必须在1-500之间", max_students)

    return result


def validate_score(data: dict) -> ValidationResult:
    """
    验证成绩数据 / Validate score data

    Args:
        data: Score data dictionary

    Returns:
        ValidationResult with any errors or warnings
    """
    result = ValidationResult()

    # student_id validation
    student_id = data.get("student_id")
    if not student_id:
        result.add_error("student_id", "学生ID不能为空", student_id)

    # course_id validation
    course_id = data.get("course_id")
    if not course_id:
        result.add_error("course_id", "课程ID不能为空", course_id)

    # score validation
    score = data.get("score")
    if score is None:
        result.add_error("score", "成绩不能为空", score)
    elif not isinstance(score, (int, float)) or score < 0 or score > 100:
        result.add_error("score", "成绩必须在0-100之间", score)
    elif score < 60:
        result.add_warning(f"成绩不及格: {score}")

    # semester validation
    semester = data.get("semester", "")
    if not semester:
        result.add_error("semester", "学期不能为空", semester)
    elif not re.match(r"^\d{4}-\d{4}-[12]$", semester):
        result.add_error("semester", "学期格式不正确，应为'YYYY-YYYY-N'（N为1或2）", semester)

    return result


def validate_dataset(records: list[dict], validator_func) -> dict:
    """
    批量验证数据集 / Validate a dataset in batch

    Args:
        records: List of data dictionaries
        validator_func: Validation function to apply

    Returns:
        Summary dictionary with validation statistics
    """
    total = len(records)
    valid_count = 0
    invalid_count = 0
    all_errors = []
    all_warnings = []

    for i, record in enumerate(records):
        result = validator_func(record)
        if result.is_valid:
            valid_count += 1
        else:
            invalid_count += 1
            for error in result.errors:
                all_errors.append({"record_index": i, "field": error.field, "message": error.message})
        all_warnings.extend(result.warnings)

    return {
        "total": total,
        "valid": valid_count,
        "invalid": invalid_count,
        "error_rate": round(invalid_count / total, 4) if total > 0 else 0,
        "errors": all_errors,
        "warnings": all_warnings,
    }
