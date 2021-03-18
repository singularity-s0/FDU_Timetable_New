# !/usr/bin/env python
# --------------------------------------------------------------
# File:          calendar.py
# Project:       FDU_Timetable
# Created:       Wednesday, 13th November 2019 5:50:47 pm
# @Author:       Molin Liu, MSc in Data Science
# Contact:          molin@live.cn
# Last Modified: Wednesday, 13th November 2019 5:50:54 pm
# Copyright  © Rockface 2019 - 2020
# --------------------------------------------------------------
# Project:      FDU_Timetable_New
# Created:      Thursday, 11th March 2021 16:25:10 pm
# Author:       Xingjian Zhao & Dong Xu, Undergraduates
# Contact:      zhaoxingjian@gmail.com
# Using the same license as the original project
# --------------------------------------------------------------

from icalendar import Calendar, Event
import datetime
import pytz
from log import LogConfig

'''
Initialize Logger
'''
logger = LogConfig('console').getLogger()
'''
FDU Course Time
'''
time_slot_start = {
    0: (8, 00),
    1: (8, 55),
    2: (9, 55),
    3: (10, 50),
    4: (11, 45),
    5: (13, 30),
    6: (14, 25),
    7: (15, 25),
    8: (16, 20),
    9: (17, 15),
    10: (18, 30),
    11: (19, 25),
    12: (20, 20)
}
s_year=0
s_month=0
s_day=0

def iso_year_start(iso_year):
    "The gregorian calendar date of the first day of the given ISO year"
    fourth_jan = datetime.date(iso_year, 1, 4)
    delta = datetime.timedelta(fourth_jan.isoweekday()-1)
    return fourth_jan - delta


def iso_to_gregorian(iso_year, iso_week, iso_day):
    "Gregorian calendar date for the given ISO year, week and day"
    year_start = iso_year_start(iso_year)
    return year_start + datetime.timedelta(days=iso_day-1, weeks=iso_week-1)


def convertDate(week, day, slot):
    '''
    Convert school week to format date.
    Parameters:
    week: week number from FDU timetable;
         教学周；
    day: day from FDU timetable;
         星期几
         Note: 0 represents Monday, 1 is Tuesday, and so forth.
         0 代表 星期一
    slot: class number in a day;
         第几节课
         Note: FDU has 14 classes a day; Class number starts with 0.
         FDU 一天14节课，从0开始。
    Returns:
    Tuple of start datetime, and end datetime. 
    A class is 45mins long.
    '''
    global s_year, s_month, s_day
    if s_year==0:
        s_year, s_month, s_day = map(int, input('\nWhen does the semester start? Answer in YYYY-MM-DD format (e.g. 2021-03-01)\n').split('-'))

    tz = pytz.timezone('Asia/Shanghai')
    corrected_time = datetime.datetime(s_year, s_month, s_day) - datetime.timedelta(days = 7)
    first_week_in_year = corrected_time.isocalendar()[1]
    week += first_week_in_year
    day = int(day)
    GC_date = iso_to_gregorian(s_year, week, day+1)
    start_hour, start_min = time_slot_start[int(slot)]
    GC_datetime = datetime.datetime.combine(
        GC_date, datetime.time(hour=start_hour, minute=start_min))
    GC_endTime = GC_datetime+datetime.timedelta(minutes=45)
    GC_datetime.replace(tzinfo=tz)
    GC_endTime.replace(tzinfo=tz)
    return GC_datetime, GC_endTime


def createCourseEvent(course, calendar):
    '''
    Create events for a course.
    为单个课程创建日历事件；

    Note: 需要注意的是本身FDU课程表数据存在重复，已经在Course类中使用
    set做了去重，但由于课程太多，没有做到一一对比。
    Note: The data from FDU teaching system exeists duplicate
    events, which has been solved in class Course. However, due
    to the tremendous courses we have, we didn't check them
    respectively.
    '''
    for week in course.available_week:
        for one_course in course.course_time:
            day, time = one_course.split(',')
            start_time, end_time = convertDate(week, day, time)
            event = Event()
            event.add('summary', course.course_name)
            event.add('dtstamp', datetime.datetime.now())
            event.add('dtstart', start_time)
            event.add('dtend', end_time)
            event.add('location', course.room_name)
            event.add('description', course.teacher_names)
            calendar.add_component(event)
    return calendar


def createCalendar(course_list):
    '''
    Create .isc file
    '''
    cal = Calendar()
    cal['version'] = '2.0'
    cal['prodid'] = '-//Fudan, ©2019 Molin. L//Timetable//CN'

    for course in course_list:
        cal = createCourseEvent(course, cal)
    '''
    生成的ics文件最好不要airdrop到手机，这样会自动添加进日历，且无法设置标记。
    建议用邮件发给自己，仅测试过系统自带邮件app，可以先确认，再添加。

    It's not recommanded to airdrop the produced ics file to your phone.
    As the result, these events will be automatically loaded to your 
    calendar, which I'm sure you will not like this, what's more, 
    you can't add tag to these events either.

    The best way to add these events is to send to your email inbox,
    open it on your phone. Recommend to use the ios default mail app.
    '''
    f = open('fdu_timetable.ics', 'wb')
    f.write(cal.to_ical())
    f.close()
    logger.info("SUCCESS: The file is saved to fdu_timetable.ics")
    input('Press ENTER to exit.')
