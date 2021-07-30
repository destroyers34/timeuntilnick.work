from flask import Flask, render_template, request
from nick import checkfornick
from virusparser import virusparser
from spamurlparser import urlparser

TimeUntilNickApp = Flask(__name__)


@TimeUntilNickApp.route("/")
def hello():
    return render_template('index.html', time=checkfornick())


@TimeUntilNickApp.route("/commercial")
def martine():
    timestring = checkfornick().split()
    time = "Commercial department will be back in " + str(int(timestring[5]) + 30) + " minute(s)"
    return render_template('index.html', time=time)


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