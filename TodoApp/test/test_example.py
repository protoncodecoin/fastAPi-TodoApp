import pytest


def test_equal_or_not_equal():
    assert 3 != 31


class Student:
    def __init__(self, first_name: str, last_name: str, major: str, year: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.year = year


@pytest.fixture
def default_employee():
    return Student("Prince", "Asante", "Computer Science", 3)


def test_person_initialization(default_employee):
    assert default_employee.first_name == "Prince", "First name should be Prince"
    assert default_employee.last_name == "Asante", "Last name should be Asante"
    assert default_employee.major == "Computer Science"
    assert default_employee.year == 3
