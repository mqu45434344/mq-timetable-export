
from operator import attrgetter
from itertools import groupby

from ._base import TimetableExporter
from ..misc import DAY_NAME_LOOKUP
from ..class_ import RegisteredClass

class Console(TimetableExporter):
    def dump(self, study_period, file):
        units = study_period.units()
        classes = [c for u in units for c in u.classes if isinstance(c, RegisteredClass)]
        classes.sort(key=attrgetter('day', 'start_time'))

        first = True
        for i, g in groupby(classes, attrgetter('day')):
            if first:
                first = False
            else:
                file.write('\n')

            print(DAY_NAME_LOOKUP[i], file=file)

            for c in g:
                unit_code = c.unit_code
                name = c.name
                class_number = c.class_number
                start_time = c.start_time.strftime('%H:%M')
                end_time = c.end_time.strftime('%H:%M')
                location = c.location
                if location.startswith('North Ryde '):
                    location = location[11:]

                file.write(f'''\
* {unit_code} {name} ({class_number})
  {start_time}-{end_time}
  {location}
''')
