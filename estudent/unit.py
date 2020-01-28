
class Unit:
    """Unit information.

    Attributes
    ----------
    name: str
        E.g., `'Systems Programming'`
    code: str
        E.g., `'COMP202'`
    period: str
        E.g., `'2019 Session 2'`
    summary: str
        A summary of the unit's classes.
    classes: List[:class:`.Class`]
        A list of classes in this unit.
    """

    def __init__(self, name, code, period, summary, classes):
        self.name = name
        self.code = code
        self.period = period
        self.summary = summary
        self.classes = classes

    def __repr__(self):
        return '<%s %r>' % (type(self).__name__,
                f'{self.code} - {self.name}')

    def _members(self):
        return (
            self.name,
            self.code,
            self.period,
            self.summary,
            self.classes,
        )

    def __eq__(self, other):
        if other.__class__ is self.__class__:
            return self._members() == other._members()
        return NotImplemented
