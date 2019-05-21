import re
import os
import logging
import datetime
from datetime import date


logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logger = logging.getLogger(__name__)


IGNORE_FILES = ['.DS_Store', '.assert']

def traverse(path):
    for fs in os.listdir(path):
        if fs in  IGNORE_FILES:
            continue
        
        if os.path.isdir(fs):
            traverse(path + '/' + fs)

        filename, file_extension = os.path.splitext(fs)
        if file_extension != '.md':
            continue

        print(filename + file_extension)
        print(os.path.abspath(fs))


REVIEW_DURATION = {'1':1, '2':3, '3':7, '4':14, '5':30, '6':60, '7':90, '8':90}


class Reminder:
    def __init__(self):
        self.today = date.today()
        self.review_need = False
        self.review_times = 1
        self.review_day = self.today

    def calc_next_review_date(self, times):
        duration = 0
        if times not in REVIEW_DURATION.keys():
            duration = REVIEW_DURATION['8']
        else:
            duration = REVIEW_DURATION[str(times)]

        return self.today + datetime.timedelta(days=duration)

    def get_yaml_formatter(self, f):
        patt_yaml = re.compile('---\n((.|\n)+)---')
        patt_review = re.compile('Review_need: (.*)\nReview_date: (.*)\nReview_times: (.*)')

        with open(f, 'r+') as fs:
            text = ''.join(fs.readlines(100))
            #  print(text)

            content =  re.match(patt_yaml, text)
            if content == None:
                return None

            return content.group(1)

    def refresh(self, f):

        patt_need = re.compile('Review_need: (.*)')
        patt_date = re.compile('Review_date: (.*)')
        patt_times = re.compile('Review_times: (.*)')
            
        ori_content = self.get_yaml_formatter(f)
        if ori_content == None:
            return

        content = ori_content.split("\n")
        print(content)

        need = [re.match(patt_need, con) for con in content]
        need = list(filter(lambda x: x != None, need))[0]

        logger.debug("Need review? {}".format(need.group(1)))
        if need.group(1) == 'False':
            return

        last_date = [re.match(patt_date, con) for con in content]
        last_date = list(filter(lambda x: x != None, last_date))[0]
        last_date_index = content.index(last_date.group(0))
        last_date = last_date.group(1)
        logger.debug("Last review date:{}".format(last_date))

        last_times = [re.match(patt_times, con) for con in content]
        last_times = list(filter(lambda x: x != None, last_times))[0]
        last_times_index = content.index(last_times.group(0))
        last_times = last_times.group(1)
        logger.debug("Last review times:{}".format(last_times))

        next_review_date = self.calc_next_review_date(last_times)
        next_review_date = 'Review_date: {}'.format(next_review_date)
        next_review_times = 'Review_times: {}'.format(int(last_times) + 1)
        logger.debug("next review date:{}, review times:{}".format(next_review_date, next_review_times))

        # update content
        content[last_date_index] = next_review_date
        content[last_times_index] = next_review_times
        content = '\n'.join(content)

        with open(f, 'r+') as fs:
            newtext = fs.read().replace(ori_content, content)


        with open(f, 'w') as fs:
            fs.write(newtext)




traverse('./')
#  reminder = Reminder()
#  reminder.refresh('Part3 Functions as Objects.md')
