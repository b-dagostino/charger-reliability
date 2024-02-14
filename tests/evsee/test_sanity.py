from pathlib import Path

import pytest
from kedro.framework.context import KedroContext
from kedro.framework.session import KedroSession
from kedro.framework.startup import bootstrap_project


@pytest.fixture
def session() -> KedroSession:
    bootstrap_project(Path.cwd())
    with KedroSession.create() as session:
        return session


@pytest.fixture
def context(session: KedroSession) -> KedroContext:
    return session.load_context()


class TestSanity:
    def test_project_path(self, session: KedroSession, context: KedroContext):
        assert context.project_path == Path.cwd()
