from flask import Flask, render_template, request, redirect, url_for
# import db_connect
# from LLM import first_chatbot
from test import test

application = Flask(__name__)

@application.route("/")
def hello():
    # instance_connection_name = "esoteric-stream-399606:asia-northeast3:wjdfoek3"
    # db_user = "postgres"
    # db_pass = "pgvectorwjdfo"
    # db_name = "pgvector"
    # vdb = db_connect(instance_connection_name, db_user, db_pass, db_name)

    return render_template("hello.html")

@application.route("/chat")
def chat():
    return render_template("chat.html")

@application.route("/qna")
def qna():
    question = request.args.get("question")
    # sep = first_chatbot("esoteric-stream-399606", "us-central1")
    # lec, prof, query_question = sep.separate(question)
    chatbot = test()
    output = chatbot.service(question)
    print(output)

    return redirect(url_for("hello"))


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=8080, debug = True)