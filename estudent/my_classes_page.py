
from .timetable_resources import _timetable_resources_from_page_source
from .misc import make_soup

class MyClassesPage:
    """
    Attributes
    ----------
    client: :class:`.Client`
    markup: str
        The 'My Classes' page source code.
    """

    def __init__(self, client, markup, soup):
        self.client = client
        self.markup = markup
        self.soup = soup

    def timetable(self):
        return _timetable_resources_from_page_source(self.client, self.soup)
