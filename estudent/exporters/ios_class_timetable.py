
# iOS app: https://apps.apple.com/au/app/class-timetable/id425121147

import datetime
import uuid
import plistlib

from ._base import TimetableExporter
from ..class_ import RegisteredClass

def seconds_since_midnight(t=None):
    if t is None:
        t = datetime.datetime.now()
    dt_combine = datetime.datetime.combine
    dummy = datetime.datetime.min
    return int((dt_combine(dummy, t) - dummy).total_seconds())

def event_color():
    for t in (
        (0, 204, 204),
        (204, 204, 255),
        (255, 153, 204),
        (204, 204, 153),
        (183, 183, 24),
        (167, 218, 100),
        (99, 158, 230),
        (232, 187, 131),
    ):
        yield tuple(i/255 for i in t)


class ClassTimetable(TimetableExporter):
    def dump(self, study_period, file):
        units = study_period.units()
        classes = [c for u in units for c in u.classes if isinstance(c, RegisteredClass)]
        unit_codes = (u.code for u in units)
        color_settings = dict(zip(unit_codes, event_color()))
        edit_date = datetime.datetime.now()

        week_events = []
        for c in classes:
            location = c.location
            if location.startswith('North Ryde '):
                location = 'U' + location[10:]

            info = '{0.name} ({0.class_number})\n{1}'.format(c, location)
            record = {
                'title': c.unit_code,
                'dayNum': (c.day - 1) % 7,
                'time': seconds_since_midnight(c.start_time),
                'endTime': seconds_since_midnight(c.end_time),
                'editDate': edit_date,
                'info': info,
                'syncID': str(uuid.uuid4()),
                'weekNum': 0,
            }
            week_events.append(record)

        plist_data = {
            'Settings': {
                'ColorSettings': color_settings,
            },
            'WeekEvents': week_events,
        }

        b = plistlib.dumps(plist_data)
        file.write(b.decode())
