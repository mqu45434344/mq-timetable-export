# MacUni eStudent timetable exporter

A Python command-line tool to extract and export timetable information from the
Macquarie Uni eStudent site. Available output formats include CSV and ICS.

The domain driven design of the codebase means that rich models make it easy
for you to roll your own exporter if the builtin formats aren’t adequate.
Take a look at the exporters and tests to get an idea of how to use the code to
create a custom export format.

## Usage

Tested on Python 3.7.6.

    python -m estudent -u45678901 -pMyPassword4 csv

If `-u` or `-p` are not specified you will be prompted to enter them. If an
export format is not specified, the default is
`console`.

Export formats:

* console
* csv
* csv2
* ics
* ios_class_timetable (https://apps.apple.com/au/app/class-timetable/id425121147)
