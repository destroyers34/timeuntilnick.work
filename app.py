from flask import Flask, render_template
from nick import checkfornick

TimeUntilNickApp = Flask(__name__)


@TimeUntilNickApp.route("/")
def hello():
    return render_template('index.html', time=checkfornick())


# return render_template('index.html')


@TimeUntilNickApp.route("/martine")
def martine():
    timestring = checkfornick().split()
    time = "Martine will be back in " + str(int(timestring[5]) + 120) + " minute(s)"
    return render_template('index.html', time=time)
    # return render_template('index.html')


if __name__ == "__main__":
    TimeUntilNickApp.run()

#test