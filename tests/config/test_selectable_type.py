import pytest

from secunit.config.one_of import OneOf
from secunit.config.utils import get_type


@pytest.fixture()
def selectable_type_a():
    TypeA = OneOf("TypeA")

    @TypeA.type
    class MockType1:
        ...

    @TypeA.type
    class MockType2:
        ...

    return TypeA


def test_selectable_type_type(selectable_type_a):
    instance_a = selectable_type_a(type="MockType1")
    assert isinstance(instance_a, "MockType1")
