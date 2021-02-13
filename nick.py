from datetime import datetime, timedelta


def untilnick():
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
    montrealtime = datetime.now()
    if montrealtime.weekday() <= 4 and (
            (6 <= montrealtime.hour < 14) or (montrealtime.hour == 14 and montrealtime.minute <= 30)):
        return True
    else:
        return False


def isnickworkingtoday():
    montrealtime = datetime.now()
    if montrealtime.weekday() <= 4 and (montrealtime.hour < 14 or (montrealtime.hour == 14 and montrealtime.minute <= 30)):
        return True
    else:
        return False


def checkfornick():
    if not isnickworking():
        print('Nick will be back in {} minute(s)'.format(untilnick()))
        return 'Nick will be back in {} minute(s)'.format(untilnick())
    else:
        print('Nick is working right now!')
        return 'Nick is working right now!'


if __name__ == '__main__':
    checkfornick()
