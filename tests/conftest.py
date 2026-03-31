"""
共享测试固件
Shared test fixtures for the graduation project data testing suite
"""

import pytest
from src.models import create_db_engine, get_session
from src.data_generator import seed_database


@pytest.fixture(scope="session")
def db_engine():
    """在内存SQLite数据库中创建测试引擎 / Create in-memory test engine"""
    engine = create_db_engine("sqlite:///:memory:")
    yield engine
    engine.dispose()


@pytest.fixture(scope="session")
def seeded_engine():
    """创建并填充测试数据的数据库引擎 / Create engine seeded with test data"""
    engine = create_db_engine("sqlite:///:memory:")
    seed_database(engine, student_count=50, score_count=200)
    yield engine
    engine.dispose()


@pytest.fixture
def session(db_engine):
    """提供干净的数据库会话，每次测试后回滚 / Provide clean session, rolled back after each test"""
    conn = db_engine.connect()
    trans = conn.begin()
    sess = get_session(db_engine)
    yield sess
    sess.close()
    trans.rollback()
    conn.close()


@pytest.fixture(scope="session")
def seeded_session(seeded_engine):
    """提供已有测试数据的数据库会话 / Provide session with pre-seeded data"""
    sess = get_session(seeded_engine)
    yield sess
    sess.close()
