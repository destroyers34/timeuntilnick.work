from datetime import datetime, timedelta


def untilnick():
    ''' This function calculates how many minutes are left before Nick is back at work
    :return: return the amount of minutes before Nick is back to work
    '''
    montrealtime = datetime.now()
    if isnickworkingtoday():
        delta = timedelta(days=-1, hours=(29 - montrealtime.hour), minutes=(60 - montrealtime.minute))
    else:
        nextweekday = montrealtime + timedelta(days=[0, 0, 0, 0, 2, 1, 0][montrealtime.weekday()],
                                           hours=(29 - montrealtime.hour),
                                           minutes=(60 - montrealtime.minute))
        delta = nextweekday - montrealtime
    return int(delta.total_seconds() // 60)


def isnickworking():
    ''' This function checks if Nick is currently working
    :return: True if Nick is working, False if not isn't working
    '''
    montrealtime = datetime.now()
    if montrealtime.weekday() <= 4 and (
            (6 <= montrealtime.hour < 14) or (montrealtime.hour == 14 and montrealtime.minute <= 30)):
        return True
    else:
        return False


def isnickworkingtoday():
    ''' This function checks if Nick is working today
    :return: True if Nick is working today, False if not isn't working today
    '''
    montrealtime = datetime.now()
    if montrealtime.weekday() <= 4 and (montrealtime.hour < 14 or (montrealtime.hour == 14 and montrealtime.minute <= 30)):
        return True
    else:
        return False


def checkfornick():
    ''' This function checks the time before Nick is back at work
    :return: The numbers of minutes before Nick works, otherwise returns -1 if Nick is currently working
    '''
    if not isnickworking():
        return untilnick()
    else:
        return -1


if __name__ == '__main__':
    checkfornick()
