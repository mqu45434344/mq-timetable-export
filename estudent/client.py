
import requests

from .misc import LOGIN_URL, TIMETABLE_URL, make_soup
from .exceptions import LoginError
from .my_classes_page import MyClassesPage


class Client:
    """Represents a client connection providing access to the eStudent site."""

    TIMEOUT = 8

    def __init__(self):
        self.session = requests.Session()

    def request(self, verb, url, *args, timeout=TIMEOUT, **kwargs):
        return self.session.request(verb, url, *args, timeout=timeout, **kwargs)

    def _aspnet_viewstate_params(self, soup):
        param_names = ('__VIEWSTATE', '__VIEWSTATEGENERATOR', '__EVENTVALIDATION')
        return {n: soup.find(id=n)['value'] for n in param_names}

    def login(self, username, password):
        """
        Parameters
        ----------
        username: str
            Your student ID.
        password: str
            Your eStudent password.
        """
        resp = self.request('GET', LOGIN_URL, timeout=self.TIMEOUT)
        soup = make_soup(resp.text)

        data = {
            '__EVENTTARGET': 'ctl00$Content$cmdLogin',
            '__EVENTARGUMENT': '',
            'ctl00$Content$txtUserName$txtText': username,
            'ctl00$Content$txtPassword$txtText': password,
            **self._aspnet_viewstate_params(soup),
        }
        resp = self.request('POST', LOGIN_URL, data=data, allow_redirects=False, timeout=self.TIMEOUT)
        if resp.status_code != 302:
            raise LoginError(resp)

    def fetch_my_classes_page(self):
        resp = self.request('GET', TIMETABLE_URL)
        resp.raise_for_status()

        text = resp.text
        soup = make_soup(text)
        if soup.select_one('#loginFormHeader'):
            raise RuntimeError('call `self.login()` first')
        return MyClassesPage(self, text, soup)


'''
print('TEST CLIENT ENABLED')
from pathlib import Path
RESOURCES_DIR = Path(__file__).parent.parent/'tests'/'files'
MY_CLASSES_HTML_FILE = RESOURCES_DIR/'45434344_2019-s1.html'

class Client(Client):
    def __init__(self):
        self.session = None

    def login(self, username, password):
        pass

    def fetch_my_classes_page(self):
        with open(MY_CLASSES_HTML_FILE) as fh:
            page = fh.read()
        return MyClassesPage(self, page)
'''#'''
