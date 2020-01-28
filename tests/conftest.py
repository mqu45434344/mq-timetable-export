
from pathlib import Path
import pytest
from estudent.my_classes_page import MyClassesPage
from estudent.misc import make_soup

RESOURCES_DIR = Path(__file__).parent/'files'
MY_CLASSES_HTML_FILE = RESOURCES_DIR/'45434344_2019-s1.html'

@pytest.fixture(scope='session')
def my_classes_page():
    content = MY_CLASSES_HTML_FILE.read_text()
    return MyClassesPage(None, content, make_soup(content))

@pytest.fixture(scope='session')
def timetable_resources(my_classes_page):
    return my_classes_page.timetable()

@pytest.fixture(scope='session')
def study_period(timetable_resources):
    return timetable_resources.study_period()

@pytest.fixture(scope='session')
def units(study_period):
    return study_period.units()

@pytest.fixture(scope='session')
def classes(study_period):
    return study_period.classes()

@pytest.fixture(scope='session')
def unit_comp225(units):
    return units[0]

@pytest.fixture(scope='session')
def class_comp225(unit_comp225):
    return unit_comp225.classes[0]
