"""A module to write to CSV log files."""

import csv
from datetime import datetime

LOG_FILE = "haocheng_s0.csv"


def _get_date() -> str:
    """Returns the current date as a string."""
    return str(datetime.now().date())


def get_date() -> str:
    """Gets the date of the event."""
    duration = input('Enter date for current log in DDMM format, leave empty for current date: ')
    if not duration:
        return _get_date()
    try:
        a = datetime.strptime(duration + f'{datetime.now().year}', '%d%m%Y')
    except ValueError:
        print('Invalid date format, try again.\n')
        return get_date()
    return str(a.date())


def get_duration() -> str:
    """Gets the duration of the event."""
    time = input('Enter duration in minutes: ')
    try:
        time = int(time)
        minutes = time % 60
        hours = time // 60
    except ValueError:
        print('Input an integer.\n')
        return get_duration()
    return f'{hours} hours, {minutes} minutes'


def get_work_done() -> str:
    """Gets the work done for the event."""
    work_done = input('Enter work done: ')
    return work_done if work_done else '-'


def get_details() -> str:
    """Gets the details for the event."""
    details = input('Enter any additional details, or leave empty: ')
    return details if details else '-'


if __name__ == '__main__':
    try:
        open(LOG_FILE, 'r').close()
    except FileNotFoundError:
        open(LOG_FILE, 'w').close()
    lst = [get_date(), get_duration(), get_work_done(), get_details()]
    with open(LOG_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(lst)
    print(f'\nWrite to "{LOG_FILE}" successful, make sure you wrote to the correct file.')
