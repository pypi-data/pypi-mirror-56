from datetime import datetime


def formatdatetimestring(datetimes):
    datetime_object = datetime.isoformat(datetimes)
    datetime_split = datetime_object.split(".")

    return datetime_split[0]


#print(datetime.now())
#print(formatdatetimestring(datetime.now()))