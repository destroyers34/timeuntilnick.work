from flask import Flask, render_template, request, abort
from nick import checkfornick
from virusparser import virusparser
from spamurlparser import urlparser
from ph_twitterbot import check_tweet
import atexit
from apscheduler.schedulers.background import BackgroundScheduler


application = Flask(__name__)


@application.errorhandler(403)
def page_not_found(e):
    return render_template('errors/403.html'), 403


@application.before_request
def limit_remote_addr():
    if request.remote_addr != '199.188.220.242' and request.remote_addr != '127.0.0.1':
        print(request.remote_addr)
        abort(403)  # Forbidden


@application.route("/")
def hello():
    time = checkfornick()
    if time == -1:
        return render_template('index.html', time='Nick is working right now!')
    else:
        return render_template('index.html', time='Nick will be back in {} minute(s)'.format(time))


@application.route("/commercial")
def commercial():
    time = checkfornick()
    if time == -1:
        return render_template('index.html', time='Commercial department is open right now!')
    else:
        return render_template('index.html', time='Commercial department will be back in {} minute(s)'.format(str(int(time)+30)))


@application.route('/virusform')
def virusform():
    return render_template('form.html')


@application.route('/results/', methods=['POST', 'GET'])
def virusdata():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form
        results = virusparser(form_data["virus"])
        return render_template('data.html', results=results)


@application.route('/spamurlparser')
def spamurlparser():
    return render_template('spamurlparser/form.html')


@application.route('/spamurlparser/results/', methods=['POST', 'GET'])
def parsedurls():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/spamurlparser' to submit form"
    if request.method == 'POST':
        form_data = request.form
        results = urlparser(form_data["urls"]).split("\n")
        return render_template('spamurlparser/data.html', results=results)


def refreshnewtweet():
    check_tweet()
    print("New Tweet Checked")


scheduler = BackgroundScheduler()
scheduler.add_job(func=refreshnewtweet, trigger="interval", seconds=60)
scheduler.start()

atexit.register(lambda: scheduler.shutdown())


if __name__ == "__main__":
    application.run()

