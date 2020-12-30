import datetime
import re
import sys

format = re.compile("^(0[1-9]|1[012])/(0[1-9]|[12][0-9]|3[01])/\d\d\d\d$")
weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def get_date(date):
    if re.fullmatch(format, date) is None:
        return None
    else:
        try:
            arr = date.split("/")
            valid_date = datetime.datetime(int(arr[2]), int(arr[0]), int(arr[1]))
        except ValueError:
            return None
        return weekdays[valid_date.weekday()] + ", " + months[int(arr[0])-1] + " " + arr[1] + ", " + arr[2]


def main():
    if len(sys.argv) != 2:
        print("None")
    else:
        date = sys.argv[1]
        print(get_date(date))

    exit()


if __name__ == '__main__':
    main()