from flask import Flask, render_template, request, abort
from nick import checkfornick
from virusparser import virusparser
from spamurlparser import urlparser

TimeUntilNickApp = Flask(__name__)


@TimeUntilNickApp.errorhandler(403)
def page_not_found(e):
    return render_template('errors/403.html'), 403


@TimeUntilNickApp.before_request
def limit_remote_addr():
    if request.remote_addr != '199.188.220.242' and request.remote_addr != '127.0.0.1':
        print(request.remote_addr)
        abort(403)  # Forbidden


@TimeUntilNickApp.route("/")
def hello():
    time = checkfornick()
    if time == -1:
        return render_template('index.html', time='Nick is working right now!')
    else:
        return render_template('index.html', time='Nick will be back in {} minute(s)'.format(time))


@TimeUntilNickApp.route("/commercial")
def commercial():
    time = checkfornick()
    if time == -1:
        return render_template('index.html', time='Commercial department is open right now!')
    else:
        return render_template('index.html', time='Commercial department will be back in {} minute(s)'.format(str(int(time)+30)))


@TimeUntilNickApp.route('/virusform')
def virusform():
    return render_template('form.html')


@TimeUntilNickApp.route('/results/', methods=['POST', 'GET'])
def virusdata():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form
        results = virusparser(form_data["virus"])
        return render_template('data.html', results=results)


@TimeUntilNickApp.route('/spamurlparser')
def spamurlparser():
    return render_template('spamurlparser/form.html')


@TimeUntilNickApp.route('/spamurlparser/results/', methods=['POST', 'GET'])
def parsedurls():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/spamurlparser' to submit form"
    if request.method == 'POST':
        form_data = request.form
        results = urlparser(form_data["urls"]).split("\n")
        return render_template('spamurlparser/data.html', results=results)


if __name__ == "__main__":
    TimeUntilNickApp.run()

