"""
数据分析测试
Tests for data analysis and statistics functions
"""

import pytest
from src.analyzer import (
    get_score_statistics,
    get_score_distribution,
    get_top_courses_by_avg_score,
    get_major_score_comparison,
    get_student_gpa,
    get_semester_trends,
)


class TestScoreStatistics:
    """成绩统计测试 / Score statistics tests"""

    def test_statistics_returns_expected_keys(self, seeded_session):
        stats = get_score_statistics(seeded_session)
        assert "count" in stats
        assert "mean" in stats
        assert "median" in stats
        assert "stdev" in stats
        assert "min" in stats
        assert "max" in stats
        assert "pass_rate" in stats
        assert "excellent_rate" in stats

    def test_count_is_positive(self, seeded_session):
        stats = get_score_statistics(seeded_session)
        assert stats["count"] > 0

    def test_mean_in_valid_range(self, seeded_session):
        stats = get_score_statistics(seeded_session)
        assert 0 <= stats["mean"] <= 100

    def test_min_max_valid(self, seeded_session):
        stats = get_score_statistics(seeded_session)
        assert stats["min"] >= 0
        assert stats["max"] <= 100
        assert stats["min"] <= stats["mean"] <= stats["max"]

    def test_pass_rate_between_0_and_1(self, seeded_session):
        stats = get_score_statistics(seeded_session)
        assert 0 <= stats["pass_rate"] <= 1

    def test_excellent_rate_lte_pass_rate(self, seeded_session):
        stats = get_score_statistics(seeded_session)
        assert stats["excellent_rate"] <= stats["pass_rate"]

    def test_pass_fail_counts_sum_to_total(self, seeded_session):
        stats = get_score_statistics(seeded_session)
        assert stats["pass_count"] + stats["fail_count"] == stats["count"]


class TestScoreDistribution:
    """成绩分布测试 / Score distribution tests"""

    def test_distribution_has_all_bands(self, seeded_session):
        dist = get_score_distribution(seeded_session)
        expected_bands = [
            "优秀(90-100)",
            "良好(80-89)",
            "中等(70-79)",
            "及格(60-69)",
            "不及格(0-59)",
        ]
        for band in expected_bands:
            assert band in dist

    def test_distribution_counts_sum_to_total(self, seeded_session):
        stats = get_score_statistics(seeded_session)
        dist = get_score_distribution(seeded_session)
        total_in_dist = sum(v["count"] for v in dist.values())
        assert total_in_dist == stats["count"]

    def test_distribution_percentages_approx_100(self, seeded_session):
        dist = get_score_distribution(seeded_session)
        total_pct = sum(v["percentage"] for v in dist.values())
        assert abs(total_pct - 100.0) < 1.0  # allow small rounding error

    def test_distribution_no_negative_counts(self, seeded_session):
        dist = get_score_distribution(seeded_session)
        for band_data in dist.values():
            assert band_data["count"] >= 0


class TestTopCourses:
    """顶尖课程测试 / Top courses tests"""

    def test_returns_list(self, seeded_session):
        results = get_top_courses_by_avg_score(seeded_session)
        assert isinstance(results, list)

    def test_limited_by_top_n(self, seeded_session):
        results = get_top_courses_by_avg_score(seeded_session, top_n=3)
        assert len(results) <= 3

    def test_default_top_5(self, seeded_session):
        results = get_top_courses_by_avg_score(seeded_session)
        assert len(results) <= 5

    def test_result_has_required_keys(self, seeded_session):
        results = get_top_courses_by_avg_score(seeded_session, top_n=1)
        if results:
            assert "course_name" in results[0]
            assert "course_code" in results[0]
            assert "avg_score" in results[0]
            assert "student_count" in results[0]

    def test_ordered_by_score_descending(self, seeded_session):
        results = get_top_courses_by_avg_score(seeded_session, top_n=5)
        scores = [r["avg_score"] for r in results]
        assert scores == sorted(scores, reverse=True)


class TestMajorComparison:
    """专业对比测试 / Major comparison tests"""

    def test_returns_list(self, seeded_session):
        results = get_major_score_comparison(seeded_session)
        assert isinstance(results, list)

    def test_result_has_required_keys(self, seeded_session):
        results = get_major_score_comparison(seeded_session)
        if results:
            assert "major" in results[0]
            assert "avg_score" in results[0]
            assert "score_count" in results[0]
            assert "student_count" in results[0]

    def test_avg_scores_in_valid_range(self, seeded_session):
        results = get_major_score_comparison(seeded_session)
        for r in results:
            assert 0 <= r["avg_score"] <= 100

    def test_ordered_by_score_descending(self, seeded_session):
        results = get_major_score_comparison(seeded_session)
        scores = [r["avg_score"] for r in results]
        assert scores == sorted(scores, reverse=True)


class TestStudentGPA:
    """学生GPA测试 / Student GPA tests"""

    def test_gpa_for_student_with_scores(self, seeded_session):
        from src.models import Score
        score_row = seeded_session.query(Score).first()
        if score_row:
            result = get_student_gpa(seeded_session, score_row.student_id)
            assert result["gpa"] >= 0
            assert result["course_count"] > 0

    def test_gpa_for_nonexistent_student(self, seeded_session):
        result = get_student_gpa(seeded_session, student_db_id=999999)
        assert result["gpa"] == 0
        assert result["course_count"] == 0

    def test_gpa_in_valid_range(self, seeded_session):
        from src.models import Score
        score_row = seeded_session.query(Score).first()
        if score_row:
            result = get_student_gpa(seeded_session, score_row.student_id)
            assert 0 <= result["gpa"] <= 100


class TestSemesterTrends:
    """学期趋势测试 / Semester trends tests"""

    def test_returns_list(self, seeded_session):
        results = get_semester_trends(seeded_session)
        assert isinstance(results, list)

    def test_has_required_keys(self, seeded_session):
        results = get_semester_trends(seeded_session)
        for r in results:
            assert "semester" in r
            assert "avg_score" in r
            assert "score_count" in r

    def test_avg_scores_in_valid_range(self, seeded_session):
        results = get_semester_trends(seeded_session)
        for r in results:
            assert 0 <= r["avg_score"] <= 100

    def test_sorted_chronologically(self, seeded_session):
        results = get_semester_trends(seeded_session)
        semesters = [r["semester"] for r in results]
        assert semesters == sorted(semesters)
