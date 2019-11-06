import time


def parse_time(ctime):
    ctime = int(ctime)
    time_struct = time.strptime(time.ctime(ctime), '%a %b %d %H:%M:%S %Y')
    time_final = time.strftime("%Y-%m-%d %H:%M", time_struct)
    return time_final


def get_today_date():
    today_time = time.strftime("%Y%m%d", time.localtime(time.time()))  # 这里涉及到时区问题，dockers默认创建的容器是UTC,可以修改容器的etc/timezone中的时区，或者这里加3600*8
    return today_time


def get_yesterday_date():
    yesterday_date = time.strftime("%Y%m%d", time.localtime(time.time()-86400))
    return yesterday_date
