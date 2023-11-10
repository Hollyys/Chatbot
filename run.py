from flask import Flask, render_template, request, redirect, url_for
import sys
import PgVector
import db_connect

application = Flask(__name__)

@application.route("/")
def hello():
    db_connect()
    return render_template("hello.html")

@application.route("/chat")
def chat():
    return render_template("chat.html")

@application.route("/qna")
def qna():
    question = request.args.get("question")
    

    return redirect(url_for("hello"))


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=8080, debug = True)