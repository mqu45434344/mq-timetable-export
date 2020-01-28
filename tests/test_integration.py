
import datetime

class TestTimetableIntegration:
    def test_timetable_resources(self, timetable_resources):
        assert timetable_resources.study_period_filters == {
            'All': '0--Feb 26, 2019',
            '2019 All Study Periods': '2019--Feb 26, 2019',
            '2019 Session 1': '2019-FHFYR-Feb 26, 2019',
        }

    def test_study_period(self, study_period):
        assert study_period.name == '2019 Session 1'

    def test_unit(self, unit_comp225):
        assert unit_comp225.name == 'Algorithms and Data Structures'
        assert unit_comp225.code == 'COMP225'
        assert unit_comp225.period == '2019 Session 1'
        assert unit_comp225.summary == ('One Weekly 115-Minutes Practical_1, '
                'One Weekly 55-Minutes Lecture_2, One Weekly 115-Minutes Lecture_1')
        assert len(unit_comp225.classes) == 3

    def test_classes(self, class_comp225):
        assert class_comp225.name == 'Practical_1'
        assert class_comp225.unit_code == 'COMP225'
        assert class_comp225.class_number == 10
        assert class_comp225.location == 'North Ryde 9 Wallys Wlk 123 Faculty PC Lab'
        assert class_comp225.day == 3
        assert class_comp225.start_date == datetime.date(2019, 2, 27)
        assert class_comp225.end_date == datetime.date(2019, 6, 5)
        assert class_comp225.start_time == datetime.time(16, 0)
        assert class_comp225.end_time == datetime.time(17, 55)
        assert class_comp225.flags == 3
        assert class_comp225.get_duration() == datetime.timedelta(seconds=6900)
