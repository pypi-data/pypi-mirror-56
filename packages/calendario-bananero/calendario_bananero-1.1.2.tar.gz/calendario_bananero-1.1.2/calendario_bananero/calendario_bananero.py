import math
from datetime import datetime, timedelta
from epiweeks import Week, Year


"""
We have a default dictionary with the initial dates of each year.
dates : {year: start_date ...}
tz: pytz object
"""


class CalendarioBananero:
    def __init__(self, dates):
        self.dates = dates

    def get_leap(self, year):
        date = self.dates[year]
        starting_day_of_year = Week(year, 1).startdate()
        diff = date - starting_day_of_year

        return diff

    def get_weekdates_range(self, year, week):
        firstdayofweek = Week(int(year), int(week)).startdate()
        lastdayofweek = firstdayofweek + timedelta(days=6.9)

        leap = self.get_leap(year)

        if leap != timedelta(0):
            firstdayofweek = firstdayofweek + timedelta(days=leap.days)
            lastdayofweek = lastdayofweek + timedelta(days=leap.days)
        else:
            firstdayofweek = firstdayofweek + timedelta(days=leap.days)
            lastdayofweek = lastdayofweek + timedelta(days=leap.days)

        return (firstdayofweek, lastdayofweek)

    def get_week_from_date(self, year, date):
        leap = self.get_leap(year)
        epi_date = date + timedelta(days=leap.days)
        epi_week = Week.fromdate(epi_date)
        return epi_week.week

    def get_period_from_date(self, year, date):
        leap = self.get_leap(year)
        epi_date = date + timedelta(days=leap.days)
        epi_week = Week.fromdate(epi_date)
        week = epi_week.week
        return math.ceil(week/3)

    def get_periods_date_range(self, year, period):
        semanas = [period * 3 - 2, period * 3 - 1, period * 3]
        fechas = [self.get_weekdates_range(year, semana) for semana in semanas]

        return [fechas[0][0], fechas[len(fechas) - 1][1]]

    def get_last_date(self, year):
        if(self.dates.get(int(year) + 1) is not None):
            return self.dates.get(int(year) + 1) - timedelta(days=1)
        else:
            return datetime.now().date().replace(
                year=int(year) + 1, month=1, day=1)

    def get_date_range_from_year(self, year):
        last_date = None
        if(self.dates.get(int(year) + 1) is not None):
            last_date = self.dates.get(int(year) + 1) - timedelta(days=1)
        else:
            last_date = datetime.now().date().replace(
                year=int(year) + 1, month=1, day=1)

        return [self.dates[year], last_date]
