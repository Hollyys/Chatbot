from flask import Flask, render_template
import sys
import PgVector

application = Flask(__name__)


@application.route("/")
def hello():
    return render_template("chat.html")


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5500, debug = True)