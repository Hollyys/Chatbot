from flask import Flask, request, jsonify
from flask_cors import CORS
# text-bison을 사용하여 결과값을 반환하는 test.py 파일의 test Class 임포트
from test import test

app = Flask(__name__)
CORS(app)

question_history = []

@app.route('/', methods=['GET', 'POST'])
def start():
    if request.method == 'GET':
        return jsonify({"question_history": question_history})

    if request.method == 'POST':
        data = request.json
        question = data.get("question")
        question_history.append(question)

        print(question, " 수신함")

        chatbot = test()
        answer = chatbot.service(question)

        print(answer, " 추출함")
        
        response_data = {"question": question, "answer": answer}
        return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')