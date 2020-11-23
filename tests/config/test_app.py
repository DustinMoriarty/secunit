from logging import DEBUG

import pytest

from secunit.config.app import App
from secunit.config.selectable_type import SelectableType
from secunit.utils import default_logger


@pytest.fixture()
def app():
    logger = default_logger("test", DEBUG)
    app = App(logger=logger)
    MockComponent = app.selectable_component("MockComponent")

    @MockComponent.type
    @app.component(arg1=int, arg2=float, kwarg1=int, kwarg2=str)
    class MockComponentA:
        def __init__(self, arg1, arg2, kwarg1=None, kwarg2=None):
            self.arg1 = arg1
            self.arg2 = arg2
            self.kwarg1 = kwarg1
            self.kwarg2 = kwarg2

    @MockComponent.type
    @app.component(arg3=int, arg4=float)
    class MockComponentB:
        def __init__(self, arg3, arg4):
            self.arg3 = arg3
            self.arg4 = arg4

    @app.component(child_component=MockComponentA)
    class MockParentComponent:
        def __init__(self, child_component: MockComponentA):
            self.child_component = child_component

    @app.component()
    class MockParentComponentDynamic:
        def __init__(self, child_component: MockComponentA):
            self.child_component = child_component

    @app.component(child_component=MockComponent)
    class MockParentComponentSelectable:
        def __init__(self, child_component: MockComponent):
            self.child_component = child_component

    return app


@pytest.fixture()
def mock_component_a_context():
    return {"arg1": 1, "arg2": 2.1, "kwarg1": 3, "kwarg2": "cow"}


@pytest.fixture()
def mock_component_b_context():
    return {"arg3": 4, "arg4": 5.5}


@pytest.fixture()
def mock_parent_context(mock_component_a_context):
    return {"child_component": mock_component_a_context}


@pytest.fixture()
def mock_parent_selectable_a_context(mock_component_a_context):
    mock_component_a_context["type"] = "MockComponentA"
    ret = {"child_component": mock_component_a_context}
    return ret


def test_app(mock_component_a_context, app):
    mock_component = app.build("MockComponentA", mock_component_a_context)
    assert int(mock_component_a_context["arg1"]) == mock_component.arg1
    assert float(mock_component_a_context["arg2"]) == mock_component.arg2
    assert int(mock_component_a_context["kwarg1"]) == mock_component.kwarg1
    assert str(mock_component_a_context["kwarg2"]) == mock_component.kwarg2


def test_app_parent_component(mock_parent_context, app):
    mock_parent = app.build("MockParentComponent", mock_parent_context)
    mock_component = mock_parent.child_component
    mock_component_context = mock_parent_context["child_component"]
    assert int(mock_component_context["arg1"]) == mock_component.arg1
    assert float(mock_component_context["arg2"]) == mock_component.arg2
    assert int(mock_component_context["kwarg1"]) == mock_component.kwarg1
    assert str(mock_component_context["kwarg2"]) == mock_component.kwarg2


def test_app_parent_component_selectable(mock_parent_selectable_a_context, app):
    mock_parent = app.build(
        "MockParentComponentSelectable", mock_parent_selectable_a_context
    )
    mock_component = mock_parent.child_component
    mock_component_context = mock_parent_context["child_component"]
    assert int(mock_component_context["arg1"]) == mock_component.arg1
    assert float(mock_component_context["arg2"]) == mock_component.arg2
    assert int(mock_component_context["kwarg1"]) == mock_component.kwarg1
    assert str(mock_component_context["kwarg2"]) == mock_component.kwarg2
