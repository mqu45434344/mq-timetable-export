
import sys
import os.path as op
sys.path.insert(1, op.abspath(op.join(__file__, *(op.pardir,)*2)))
import estudent
del sys.path[1]

client = estudent.Client()
client.login('', '')

my_classes_page = client.fetch_my_classes_page()
timetable_resources = my_classes_page.timetable()
study_period = timetable_resources.study_period()
units = study_period.units()
unit = units[0]
classes = [c for u in units for c in u.classes]
klass = classes[0]

print(client)
print(my_classes_page)
print(timetable_resources)
print(study_period)
print(unit)
print(klass)
