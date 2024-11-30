import argparse
import csv
import sys
from datetime import datetime, timedelta

# Set up argument parser
parser = argparse.ArgumentParser(description="Extract event start dates from CSV file")
parser.add_argument('filename', type=str, help="The path to the CSV file")
parser.add_argument('starting_id', type=int, help="The ID of the first practice")

# Parse the arguments
args = parser.parse_args()

# Check if filename was provided
if not args.filename:
    print("Error: CSV filename is required as a command-line argument.")
    sys.exit(1)

# Check if starting_id was provided
if not args.starting_id:
    print("Error: starting_id is required as a command-line argument.")
    sys.exit(1)


# Open the CSV file specified by the command-line argument
with open(args.filename, 'r') as csvfile:
    reader = csv.DictReader(csvfile)

    # Extract the start dates

    practice_dates = [
        datetime.strptime(row['EVENT START DATE'], "%Y/%m/%d") for row in reader
    ]


tickets_filename = "{0}-tickets.{1}".format(*args.filename.split("."))

CSV_HEADER = (
    "\"Event Name, ID, or Slug\",Ticket Name,Ticket Description,Ticket Start Sale Date,"
    "Ticket Start Sale Time,Ticket End Sale Date,Ticket End Sale Time,Ticket Stock, "
    "Ticket Price\n"
)

CSV_ROW = (
    "{_id},{ticket_name},,{start_date},{start_time},{end_date},{end_time},{ticket_count},"
    "{price}\n"
)

ticket_count = 40
price = 15
start_date = datetime.today().strftime("%Y/%m/%d")
start_time = "12:00 AM"
end_time = "12:00 AM"
one_day = timedelta(days=1)

with open(tickets_filename, 'w+') as f:
    f.write(CSV_HEADER)
    for i, practice in enumerate(practice_dates):
        _id = args.starting_id + i
        ticket_name = f"practice{practice.strftime('%Y%m%d')}"
        end_date = (practice + one_day).strftime("%Y/%m/%d")
        f.write(CSV_ROW.format(
            _id=_id,
            ticket_name=ticket_name,
            start_date=start_date,
            start_time=start_time,
            end_date=end_date,
            end_time=end_time,
            ticket_count=ticket_count,
            price=price
        ))
