import datetime
import re


def cracked_games_date_after(cracked_date, release_date):
    try:
        return calculate_date(cracked_date, release_date)
    except AttributeError:
        return '0 day'


def calculate_date(cracked_date, release_date):
    release_date = datetime.datetime.strptime(release_date.replace('-', ''), "%Y%m%d").date()
    cracked_date = datetime.datetime.strptime(cracked_date.replace('-', ''), "%Y%m%d").date()
    cracked_after = re.match(r'-{0,1}\d{1,4}\s{1}\w{3,4}', str(cracked_date - release_date)).group()

    return cracked_after


def uncracked_games_days_counting(release_date):
    release_date = datetime.datetime.strptime(release_date.replace('-', ''), "%Y%m%d").date()
    counting_date = re.match(r'-{0,1}\d{1,4}\s{1}\w{3,4}', str(datetime.date.today() - release_date)).group()

    return counting_date


def counting_days_release(release_date):
    release_date = datetime.datetime.strptime(release_date.replace('-', ''), "%Y%m%d").date()
    remain = re.match(r'-{0,1}\d{1,4}\s{1}\w{3,4}', str(release_date - datetime.date.today())).group()

    return remain
