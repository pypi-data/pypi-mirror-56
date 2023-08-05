__version__ = '0.1.0'

from datetime import date


#2015-2016
started_2015 = date(2015, 9, 1)
ended_2015 = date(2016, 9, 1)

#2016-2017
started_2016 = date(2016, 9, 1)
ended_2016 = date(2017, 9, 11)

#2017-2018
started_2017 = date(2017, 9, 11)
ended_2017 = date(2018, 9, 10)

#2018-2019
started_2018 = date(2018, 9, 10)
ended_2018 = date(2019, 9, 9)

#2019-2020
started_2019 = date(2019, 9, 9)
ended_2019 = date(2020, 8, 7)


def find_academic_year(given_date):
    try:
        if (started_2015 <= given_date < ended_2015):
            return '2015-2016'
        elif (started_2016 <= given_date < ended_2016):
            return '2016-2017'
        elif (started_2017 <= given_date < ended_2017):
            return '2017-2018'
        elif (started_2018 <= given_date < ended_2018):
            return '2018-2019'
        elif (started_2019 <= given_date < ended_2019):
            return '2019-2020'
        else:
            return None
    except:
        return "error"


if __name__ == '__main__':
    given_date = date(2019,5,3)
    result = find_academic_year(date(2019,5,3))
    print(result)
