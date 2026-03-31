"""
数据分析器
Data Analyzer - statistical analysis of student/course/score data
"""

import statistics
from collections import Counter
from sqlalchemy import func, text
from sqlalchemy.orm import Session
from src.models import Student, Course, Score


def get_score_statistics(session: Session) -> dict:
    """
    获取成绩统计信息 / Get score statistics

    Args:
        session: SQLAlchemy session

    Returns:
        Dictionary with score statistics
    """
    scores = [row[0] for row in session.query(Score.score).all()]

    if not scores:
        return {"count": 0}

    pass_count = sum(1 for s in scores if s >= 60)
    excellent_count = sum(1 for s in scores if s >= 90)

    return {
        "count": len(scores),
        "mean": round(statistics.mean(scores), 2),
        "median": round(statistics.median(scores), 2),
        "stdev": round(statistics.stdev(scores), 2) if len(scores) > 1 else 0,
        "min": min(scores),
        "max": max(scores),
        "pass_rate": round(pass_count / len(scores), 4),
        "excellent_rate": round(excellent_count / len(scores), 4),
        "pass_count": pass_count,
        "fail_count": len(scores) - pass_count,
        "excellent_count": excellent_count,
    }


def get_score_distribution(session: Session) -> dict:
    """
    获取成绩分布 / Get score distribution (grade bands)

    Args:
        session: SQLAlchemy session

    Returns:
        Dictionary with distribution by grade bands
    """
    scores = [row[0] for row in session.query(Score.score).all()]

    bands = {
        "优秀(90-100)": 0,
        "良好(80-89)": 0,
        "中等(70-79)": 0,
        "及格(60-69)": 0,
        "不及格(0-59)": 0,
    }

    for s in scores:
        if s >= 90:
            bands["优秀(90-100)"] += 1
        elif s >= 80:
            bands["良好(80-89)"] += 1
        elif s >= 70:
            bands["中等(70-79)"] += 1
        elif s >= 60:
            bands["及格(60-69)"] += 1
        else:
            bands["不及格(0-59)"] += 1

    total = len(scores)
    distribution = {
        band: {"count": count, "percentage": round(count / total * 100, 2) if total > 0 else 0}
        for band, count in bands.items()
    }

    return distribution


def get_top_courses_by_avg_score(session: Session, top_n: int = 5) -> list[dict]:
    """
    获取平均成绩最高的课程 / Get top courses by average score

    Args:
        session: SQLAlchemy session
        top_n: Number of top courses to return

    Returns:
        List of course dictionaries with average scores
    """
    results = (
        session.query(
            Course.course_name,
            Course.course_code,
            func.avg(Score.score).label("avg_score"),
            func.count(Score.id).label("student_count"),
        )
        .join(Score, Course.id == Score.course_id)
        .group_by(Course.id)
        .order_by(func.avg(Score.score).desc())
        .limit(top_n)
        .all()
    )

    return [
        {
            "course_name": r.course_name,
            "course_code": r.course_code,
            "avg_score": round(r.avg_score, 2),
            "student_count": r.student_count,
        }
        for r in results
    ]


def get_major_score_comparison(session: Session) -> list[dict]:
    """
    按专业统计平均成绩 / Compare average scores by major

    Args:
        session: SQLAlchemy session

    Returns:
        List of major statistics
    """
    results = (
        session.query(
            Student.major,
            func.avg(Score.score).label("avg_score"),
            func.count(Score.id).label("score_count"),
            func.count(Student.id.distinct()).label("student_count"),
        )
        .join(Score, Student.id == Score.student_id)
        .group_by(Student.major)
        .order_by(func.avg(Score.score).desc())
        .all()
    )

    return [
        {
            "major": r.major,
            "avg_score": round(r.avg_score, 2),
            "score_count": r.score_count,
            "student_count": r.student_count,
        }
        for r in results
    ]


def get_student_gpa(session: Session, student_db_id: int) -> dict:
    """
    计算学生GPA / Calculate student GPA

    Args:
        session: SQLAlchemy session
        student_db_id: Student's database ID

    Returns:
        Dictionary with GPA information
    """
    results = (
        session.query(Score.score, Course.credits)
        .join(Course, Score.course_id == Course.id)
        .filter(Score.student_id == student_db_id)
        .all()
    )

    if not results:
        return {"student_id": student_db_id, "gpa": 0, "course_count": 0}

    total_credits = sum(r.credits for r in results)
    weighted_sum = sum(r.score * r.credits for r in results)

    gpa = round(weighted_sum / total_credits, 2) if total_credits > 0 else 0

    return {
        "student_id": student_db_id,
        "gpa": gpa,
        "course_count": len(results),
        "total_credits": round(total_credits, 1),
    }


def get_semester_trends(session: Session) -> list[dict]:
    """
    按学期统计成绩趋势 / Get score trends by semester

    Args:
        session: SQLAlchemy session

    Returns:
        List of semester statistics sorted chronologically
    """
    results = (
        session.query(
            Score.semester,
            func.avg(Score.score).label("avg_score"),
            func.count(Score.id).label("score_count"),
        )
        .group_by(Score.semester)
        .order_by(Score.semester)
        .all()
    )

    return [
        {
            "semester": r.semester,
            "avg_score": round(r.avg_score, 2),
            "score_count": r.score_count,
        }
        for r in results
    ]
