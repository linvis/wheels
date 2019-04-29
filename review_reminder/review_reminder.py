import sys
import datetime
from datetime import date
from collections import defaultdict

duration = {'1':1, '2':3, '3':7, '4':14, '5':30, '6':60, '7':90, '8':90}

def calc_next_review_date(times):
    interval = 0
    if times not in duration.keys():
        interval = duration['8']
    else:
        interval = duration[times]

    return date.today() + datetime.timedelta(days=interval)


if __name__ == "__main__":
    if (len(sys.argv) <= 1):
        print("Usage: ./review_reminder.py [review times]")
        exit(0)

    print("next review date is {}".format(calc_next_review_date(sys.argv[1])))
