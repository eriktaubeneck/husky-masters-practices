import calendar
from datetime import datetime, time, timedelta
from enum import Enum

cal = calendar.Calendar()


# Define the Weekday Enum
class Weekday(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


coaches = {
    "addie": "Addie P.",
    "alex": "Alex P.",
    "erik": "Erik T.",
    "matt": "Matt J.",
    "nate": "Nate K.",
    "jamie": "Jamie C.",
}

# Set the target weekday and initialize DEFAULT_START_DATE
practice_days = [Weekday.MONDAY, Weekday.TUESDAY, Weekday.THURSDAY]
today = datetime.today()

# Move to the first day of the next month
next_month = datetime.combine(
    (today.replace(day=1) + timedelta(days=32)).replace(day=1),
    time(0, 0)
)

month_and_year = input(f"MM/YY? (Default {next_month.strftime('%m/%y')}): ")
if month_and_year == "":
    month, year = next_month.month, next_month.year
else:
    month = int(month_and_year.split("/")[0].lstrip("0"))
    century = (next_month.year//100)*100
    year = century + int(month_and_year.split("/")[1])

practice_dates = (
    d for d in
    cal.itermonthdates(year, month)
    if d.weekday() in [pd.value for pd in practice_days]
    and d.month == month
)

CSV_HEADER = (
    "EVENT NAME,EVENT EXCERPT,EVENT VENUE NAME,EVENT ORGANIZER NAME,EVENT START DATE,"
    "EVENT START TIME,EVENT END DATE,EVENT END TIME,ALL DAY EVENT,TIMEZONE,"
    "HIDE FROM EVENT LISTINGS,STICKY IN MONTH VIEW,EVENT CATEGORY,EVENT TAGS,"
    "EVENT COST,EVENT CURRENCY SYMBOL,EVENT CURRENCY POSITION,EVENT ISO CURRENCY CODE,"
    "EVENT FEATURED IMAGE,EVENT WEBSITE,EVENT SHOW MAP LINK,EVENT SHOW MAP,"
    "ALLOW COMMENTS,ALLOW TRACKBACKS AND PINGBACKS,EVENT DESCRIPTION\n"
)

CSV_ROW_TEMPLATE = (
    "{practice_title},,View Ridge Swim & Tennis Club,{coach},{start_dt},{end_dt},"
    "FALSE,America/Los_Angeles,FALSE,FALSE,Practice,,,,,,,,,FALSE,FALSE\n"
)


filename = f"{year}-{month:02d}-01-practices.csv"

with open(filename, "w+") as f:
    f.write(CSV_HEADER)
    for practice_date in practice_dates:
        practice_title = input(
            f"provide practice title (or \"skip\") for "
            f"{practice_date.strftime('%a %m-%d')}: "
        )
        if practice_title != "skip":
            coach_str = input("who's the coach? ")
            while coach_str not in coaches.keys():
                coach_str = input(
                    f"invalid selection. pick from {', '.join(coaches.keys())}: "
                )

            start_dt = datetime.combine(practice_date, time(20, 20))
            end_dt = datetime.combine(practice_date, time(21, 20))
            f.write(CSV_ROW_TEMPLATE.format(
                practice_title=practice_title,
                start_dt=start_dt.strftime("%Y/%m/%d,%-I:%M%p"),
                end_dt=end_dt.strftime("%Y/%m/%d,%-I:%M%p"),
                coach=coaches[coach_str],
            ))
