
import datetime

from ._base import TimetableExporter
from ..misc import TZ
from ..class_ import RegisteredClass

class Ics(TimetableExporter):
    def dump(self, study_period, file):
        units = study_period.units()
        classes = [c for u in units for c in u.classes if isinstance(c, RegisteredClass)]

        file.write('''\
BEGIN:VCALENDAR
VERSION:2.0
CALSCALE:GREGORIAN
''')
        for c in classes:
            location = c.location
            if location.startswith('North Ryde '):
                location = 'U' + location[10:]

            rrule_count = (c.end_date - c.start_date).days // 7 + 1
            start_datetime = datetime.datetime.combine(c.start_date, c.start_time)
            event_start = start_datetime.strftime('%Y%m%dT%H%M%S')
            event_end = start_datetime.replace(hour=c.end_time.hour, minute=c.end_time.minute) \
                    .strftime('%Y%m%dT%H%M%S')

            file.write(f'''\
BEGIN:VEVENT
TRANSP:OPAQUE
RRULE:FREQ=WEEKLY;COUNT={rrule_count}
DTSTART;TZID={TZ}:{event_start}
DTEND;TZID={TZ}:{event_end}
SUMMARY:{c.unit_code} {c.name} ({c.class_number})
LOCATION:{location}
END:VEVENT
''')

        file.write('END:VCALENDAR\n')
