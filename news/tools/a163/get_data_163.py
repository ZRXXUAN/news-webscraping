def get_date(date):
    if not date:
        return '0000-00-00 00:00'
    month = date[0:2]
    day = date[3:5]
    year = date[6:10]
    hour_minute = date[11:16]
    return year + '-' + month + '-' + day + ' ' + hour_minute
