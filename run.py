import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(__file__))

def untilnick():
    montrealtime = datetime.now()
    nextweekday = montrealtime + timedelta(days=[0, 0, 0, 0, 2, 1, 0][montrealtime.weekday()],
                                           hours=(29 - montrealtime.hour),
                                           minutes=(60 - montrealtime.minute))
    delta = nextweekday - montrealtime
    print('Nick will be back in {} minute(s)'.format(int(delta.total_seconds() // 60)))
    # print('{} ou {} secondes'.format(delta,delta.seconds))
    return 'Nick will be back in {} minute(s)'.format(int(delta.total_seconds() // 60))


def isnickworking():
    montrealtime = datetime.now()
    if montrealtime.weekday() <= 4 and ((6 <= montrealtime.hour < 14) or (montrealtime.hour == 14 and montrealtime.minute <= 30)):
        return True
    else:
        return False


def checkfornick():
    if not isnickworking():
        return untilnick()
    else:
        print('Nick is working right now!')
        return 'Nick is working right now!'



def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    message = checkfornick()
    #version = 'Python %s\n' % sys.version.split()[0]
    #response = '\n'.join([message, version])
    htmltest = open('media/main.html', 'r', encoding='utf-8')
    source_code = htmltest.read()
    htmltest.close()
    #return [source_code.encode()]
    return [HttpResponse(htmltest, content_type="text/html")]