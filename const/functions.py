import datetime

#App engine stores all time in UTC zone.
#Helper functions to convert from UTC to IST and vice-versa
IST_OFFSET_HOURS = 5.5

#Function to convert UTC to IST
def utc_to_ist(date):
    return date + datetime.timedelta(hours=IST_OFFSET_HOURS)

#Function to convert UTC to IST
def ist_to_utc(date):
    return date - datetime.timedelta(hours=IST_OFFSET_HOURS)

date_format_string = '%d-%b-%Y,%H:%M:%S'
def date_to_string(date):
    return date.strftime(date_format_string)

def string_to_date(date):
    try:
        return datetime.datetime.strptime(date, date_format_string)
    except:
        return None