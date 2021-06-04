from flask import Flask, render_template, request
from nick import checkfornick

TimeUntilNickApp = Flask(__name__)


@TimeUntilNickApp.route("/")
def hello():
    return render_template('index.html', time=checkfornick())


@TimeUntilNickApp.route("/martine")
def martine():
    timestring = checkfornick().split()
    time = "Martine will be back in " + str(int(timestring[5]) + 120) + " minute(s)"
    return render_template('index.html', time=time)


@TimeUntilNickApp.route('/virusform')
def form():
    return render_template('form.html')


@TimeUntilNickApp.route('/results/', methods=['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form
        return render_template('data.html', form_data=form_data)


if __name__ == "__main__":
    TimeUntilNickApp.run()