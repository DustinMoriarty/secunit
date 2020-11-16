from logging import DEBUG

import pytest

from secunit.config.app import App
from secunit.utils import default_logger
from secunit.config.component import Component


@pytest.fixture()
def app():
    logger = default_logger("test", DEBUG)
    app = App(logger=logger)

    @app.component(arg1=int, arg2=float, kwarg1=int, kwarg2=str)
    class MockComponent:
        def __init__(self, arg1, arg2, kwarg1=None, kwarg2=None):
            self.arg1 = arg1
            self.arg2 = arg2
            self.kwarg1 = kwarg1
            self.kwarg2 = kwarg2

    @app.component(child_component=MockComponent)
    class MockParentComponent:
        def __init__(self, child_component: MockComponent):
            self.child_component = child_component

    @app.component()
    class MockParentComponentDynamic:
        def __init__(self, child_component: MockComponent):
            self.child_component = child_component

    return app


@pytest.fixture()
def mock_component_context():
    return {"arg1": 1, "arg2": 2.1, "kwarg1": 3, "kwarg2": "cow"}


@pytest.fixture()
def mock_parent_context(mock_component_context):
    return {"child_component": mock_component_context}


@pytest.fixture()
def mock_parent_dynamic_context(mock_component_context):
    ret = {"child_component": mock_component_context}
    ret["child_component"]["type"] = "MockComponent"
    return ret


def test_app(mock_component_context, app):
    mock_component = app.build("MockComponent", mock_component_context)
    assert int(mock_component_context["arg1"]) == mock_component.arg1
    assert float(mock_component_context["arg2"]) == mock_component.arg2
    assert int(mock_component_context["kwarg1"]) == mock_component.kwarg1
    assert str(mock_component_context["kwarg2"]) == mock_component.kwarg2


def test_app_parent_component(mock_parent_context, app):
    mock_parent = app.build("MockParentComponent", mock_parent_context)
    mock_component = mock_parent.child_component
    mock_component_context = mock_parent_context["child_component"]
    assert int(mock_component_context["arg1"]) == mock_component.arg1
    assert float(mock_component_context["arg2"]) == mock_component.arg2
    assert int(mock_component_context["kwarg1"]) == mock_component.kwarg1
    assert str(mock_component_context["kwarg2"]) == mock_component.kwarg2
