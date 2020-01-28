
import datetime
from .misc import ClassFlags, DAY_ENUM_LOOKUP

strptime = datetime.datetime.strptime
dtcombine = datetime.datetime.combine
dummydt = datetime.date.min

class Class:
    """A base class for a class model."""

    def __init__(self, name, unit_code):
        self.name = name
        self.unit_code = unit_code

    def __repr__(self):
        return '<%s %r>' % (type(self).__name__,
                '%s, %s' % (self.unit_code, self.name))

    def __eq__(self, other):
        if other.__class__ is self.__class__:
            return (self.name, self.unit_code) == (other.name, other.unit_code)
        return NotImplemented

class UnregisteredClass(Class):
    """Stores information about an unregistered class.

    Attributes
    ----------
    name: str
        E.g., ``'Practical_1'``
    unit_code: str
        E.g., ``'COMP255'``
    """

class RegisteredClass(Class):
    """Stores information about a registered class.

    Attributes
    ----------
    name: str
        E.g., ``'Practical_1'``
    unit_code: str
        E.g., ``'COMP255'``
    class_number: int
        The class number.
    location: str
        The class' location.
    day: :class:`.Day`
        Day of the week.
    start_date: datetime.date
        The date when the first class starts.
    end_date: datetime.date
        The date when the last class ends.
    start_time: datetime.time
        The time the class starts.
    end_time: datetime.time
        The time the class ends.
    flags: int
        1: Registered
            You have successfully registered into this class.
        2: Swappable
            There are other available classes that you can swap into.
        4: Stream
            This class is part of a set of classes that must be taken in sync.
    """

    def __init__(self, *, name, unit_code, class_number, location, day,
            start_date, end_date, start_time, end_time, flags):
        super().__init__(name=name, unit_code=unit_code)
        self.class_number = class_number
        self.location = location
        self.day = day
        self.start_date = start_date
        self.end_date = end_date
        self.start_time = start_time
        self.end_time = end_time
        self.flags = flags

    def __repr__(self):
        return '<%s %r>' % (
                type(self).__name__,
                '%s, %s (%d)' % (self.unit_code, self.name, self.class_number))

    def _members(self):
        return (
            self.name,
            self.unit_code,
            self.class_number,
            self.location,
            self.day,
            self.start_date,
            self.end_date,
            self.start_time,
            self.end_time,
            self.flags,
        )

    def __eq__(self, other):
        if other.__class__ is self.__class__:
            return  self._members() == other._members()
        return NotImplemented

    def get_duration(self):
        return dtcombine(dummydt, self.end_time) - dtcombine(dummydt, self.start_time)


def _extract_class_info(tags, year):
    class_flag_lookup = dict(zip('cssTtableIconReg cssTtableIconSwap cssTtableIconStream'.split(), ClassFlags))

    unit_code = tags.select_one('.cssTtableSspNavMasterContainer .cssTtableSspNavMasterSpkInfo2 span').text
    classes_info = tags.select('.cssTtableSspNavDetailsContainer .cssTtableNavActvTop')

    classes = []
    for data in classes_info:
        class_name = data.find('div').get_text(strip=True)
        class_item = None
        place_time_info = data.select_one('.cssTtableNavMainText .cssTtableSspNavDiv')
        if len(place_time_info.contents) <= 1:
            class_item = UnregisteredClass(name=class_name, unit_code=unit_code)
        else:
            what = place_time_info.select_one('.cssTtableNavMainWhat')
            where = place_time_info.select_one('.cssTtableNavMainWhere')
            when = place_time_info.select_one('.cssTtableNavMainWhen')
            start_date_str, end_date_str, timeslot = map(str, when.contents[1::2])
            day_name, _, timespan_string = timeslot.partition(', ')
            starting_time, _, ending_time = timespan_string.partition('-')

            icons = data.select('.cssTtableSspNavIconTray img')
            flags = 0
            for icon in icons:
                flags |= class_flag_lookup[icon['class'][0]]

            start_date = strptime(start_date_str, '%d-%b').replace(year=year).date()
            end_date = strptime(end_date_str, '%d-%b').replace(year=year).date()
            class_item = RegisteredClass(
                name=class_name,
                unit_code=unit_code,
                class_number=int(what.text.partition(' ')[2]),
                location=str(where.contents[1]),
                day=DAY_ENUM_LOOKUP[day_name],
                start_time=strptime(starting_time, '%I:%M %p').time(),
                end_time=strptime(ending_time, '%I:%M %p').time(),
                start_date=start_date,
                end_date=end_date,
                flags=flags,
            )

        classes.append(class_item)
    return classes
