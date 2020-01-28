
import re
import datetime
from .unit import Unit
from .class_ import _extract_class_info

class StudyPeriod:
    """A study period data class.

    Attributes
    ----------
    name: str
        The name.
    """

    def __init__(self, name, units_supplier):
        self.name = name
        self._units_supplier = units_supplier

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.name!r}>'

    def units(self):
        return self._units_supplier()

def get_study_period_supplier(soup):
    def __():
        def units_supplier(year):
            def __():
                units = []
                units_container = soup.select('#ctl00_Content_ctlNav_ctl04 .cssTtableSspNavContainer')
                for tag in units_container:
                    unit_info = tag.select_one('.cssTtableSspNavMasterContainer')
                    u = Unit(
                        name=unit_info.select_one('.cssTtableSspNavMasterSpkInfo3 div').get_text(strip=True),
                        code=unit_info.select_one('.cssTtableSspNavMasterSpkInfo2 span').text,
                        period=unit_info.select_one('.cssTtableSspNavMasterSpkInfo3 span').get_text(strip=True),
                        summary=unit_info.select_one('.cssTtableSspNavMasterActvSmry div').get_text(strip=True),
                        classes=_extract_class_info(tag, year),
                    )
                    units.append(u)
                return units
            return __

        tag = soup.select_one('#ctl00_Content_ctlFilter_CboStudyPeriodFilter_elbList option[selected]')
        study_period_name = tag.text
        study_period_value = tag['value']

        # Infer the year from the study period filter list.
        year = -1
        for needle in study_period_name, study_period_value:
            m = re.match(r'\b20\d\d\b', needle)
            if m:
                year = int(m[0])
                break
        else:
            # If the year could not be determined, use the current year.
            year = datetime.datetime.now().year

        return StudyPeriod(
            name=study_period_name,
            units_supplier=units_supplier(year),
        )
    return __
