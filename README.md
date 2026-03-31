# GraduationProjectDataTesting
毕业设计数据测试

A Python-based data testing framework for a graduation project. It covers data generation, validation, database CRUD testing, and statistical analysis for a student information management scenario.

## Project Structure

```
GraduationProjectDataTesting/
├── src/
│   ├── __init__.py
│   ├── models.py          # SQLAlchemy ORM models (Student, Course, Score)
│   ├── data_generator.py  # Realistic test data generator
│   ├── validators.py      # Data validation rules and business logic
│   └── analyzer.py        # Statistical analysis functions
├── tests/
│   ├── __init__.py
│   ├── conftest.py                # Shared pytest fixtures
│   ├── test_validators.py         # Data validation tests
│   ├── test_database.py           # Database CRUD tests
│   ├── test_data_generator.py     # Data generator tests
│   └── test_analyzer.py           # Statistical analysis tests
├── reports/                       # Test coverage reports (generated)
├── requirements.txt
├── pytest.ini
└── README.md
```

## Features

- **Data Models**: `Student`, `Course`, and `Score` ORM models backed by SQLite
- **Data Generator**: Produces realistic Chinese student/course/score data using Faker
- **Data Validators**: Field-level validation with error and warning reporting, batch dataset validation
- **Data Analyzer**: Score statistics, grade distribution, GPA calculation, major comparison, semester trends
- **Test Suite**: 113 pytest tests covering all modules with ≥ 94% code coverage

## Getting Started

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run tests

```bash
pytest
```

### Run tests with HTML coverage report

```bash
pytest --cov=src --cov-report=html:reports/coverage
```

The HTML coverage report is written to `reports/coverage/index.html`.

## Test Coverage

| Module               | Coverage |
|----------------------|----------|
| `src/models.py`      | 92%      |
| `src/data_generator.py` | 95%   |
| `src/validators.py`  | 94%      |
| `src/analyzer.py`    | 98%      |
| **Total**            | **94%**  |
