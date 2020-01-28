
from .misc import TIMETABLE_URL, make_soup
from .study_period import get_study_period_supplier

class TimetableResources:
    """A class that stores some timetable-related state and provides domain objects.

    Attributes
    ----------
    client: :class:`.Client`
    study_period_filters: Dict[str, str]
        Values can be used in :meth:`fetch_study_period`.
    """

    def __init__(self, client, soup, study_period_filters, study_period_supplier):
        self.client = client
        self._soup = soup
        self.study_period_filters = study_period_filters
        self._study_period_supplier = study_period_supplier

    def study_period(self):
        return self._study_period_supplier()

    def fetch_study_period(self, value):
        data = {
            'ctl00$Content$ctlFilter$CboStudyPeriodFilter$elbList': value,
            **self.client._aspnet_viewstate_params(self._soup),
        }
        resp = self.client.request('POST', TIMETABLE_URL, data=data, allow_redirects=False)
        resp.raise_for_status()
        soup = make_soup(resp.text)
        return get_study_period_supplier(soup)()


def _timetable_resources_from_page_source(client, soup):
    filter_options = soup.select('#ctl00_Content_ctlFilter_CboStudyPeriodFilter_elbList option')
    study_period_filters = {tag.text: tag['value'] for tag in filter_options}
    return TimetableResources(
        client,
        soup,
        study_period_filters=study_period_filters,
        study_period_supplier=get_study_period_supplier(soup),
    )
