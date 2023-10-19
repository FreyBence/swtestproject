from datetime import date
import calendar

months = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
]


def days(year, month):
    return calendar.monthcalendar(year, month)


def today():
    day = date.today()
    return str(day).split('-')
