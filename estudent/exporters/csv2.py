
import csv
from ._base import TimetableExporter
from ..class_ import RegisteredClass

class Csv2(TimetableExporter):
    def __init__(self, **writer_options):
        if 'quoting' not in writer_options:
            writer_options['quoting'] = csv.QUOTE_ALL
        self.writer_options = writer_options

    def dump(self, study_period, file):
        writer = csv.writer(file, **self.writer_options)
        writerow = writer.writerow

        units = study_period.units()
        classes = [c for u in units for c in u.classes if isinstance(c, RegisteredClass)]

        writerow('unit_code name class_number flags start_date end_date day start_time end_time location'.split())
        for c in classes:
            row = (
                c.unit_code,
                c.name,
                c.class_number,
                int(c.flags),
                str(c.start_date),
                str(c.end_date),
                c.day.value,
                c.start_time.strftime('%H:%M'),
                c.end_time.strftime('%H:%M'),
                (c.location[11:] if c.location.startswith('North Ryde ') else c.location),
            )
            writerow(row)
