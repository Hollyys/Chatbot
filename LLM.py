import vertexai
from transformers import AutoModel, AutoTokenizer
from vertexai.preview.language_models import ChatModel, InputOutputTextPair, ChatMessage
from db_connect import db_connect

# PROJECT_ID = "esoteric-stream-399606"
# LOCATION = "us-central1"
instance_connection_name = "esoteric-stream-399606:asia-northeast3:wjdfoek3"
db_user = "postgres"
db_pass = "pgvectorwjdfo"
db_name = "pgvector"
vdb = db_connect(instance_connection_name, db_user, db_pass, db_name)

class first_chatbot:
    def __init__(self, proj_id, loc):
        vertexai.init(project = proj_id, location = loc)

    @staticmethod
    def get_KoSimCSE():
        model = AutoModel.from_pretrained('BM-K/KoSimCSE-roberta-multitask')
        tokenizer = AutoTokenizer.from_pretrained('BM-K/KoSimCSE-roberta-multitask')

        return model, tokenizer

    def separate(self, question):
        model, tokenizer = get_KoSimCSE()
        query_text = input("Q >> ")

        chat_model = ChatModel.from_pretrained("chat-bison@001")  #chat model 불러오기

        chat = chat_model.start_chat(
            context="수업에 대해 궁금해하는 학생들이 과목, 교수에 대해 질문하는 서비스야. 강의평과 관련된 질문이면 질문 내용에 질문을 출력해주고 아니면 그냥 NULL을 출력해줘",
            examples=[
                InputOutputTextPair(
                    input_text="정기숙 교수님 자료구조응용 수업 어때?에서 과목명, 교수명, 질문 내용이 뭐야?",
                    output_text="과목명 자료구조응용 교수명 정기숙 질문 내용 수업이 어떤지 물어보는 내용",
                ),
                InputOutputTextPair(
                    input_text="정기숙 교수님 어때?에서 과목명, 교수명, 질문내용이 뭐야?",
                    output_text="과목명 NULL 교수명 정기숙 질문 내용 교수님이 어떤지 물어보는 내용",
                ),
                InputOutputTextPair(
                    input_text="자료구조응용 수업 어때?에서 과목명, 교수명, 질문내용이 뭐야?",
                    output_text="과목명 자료구조응용 교수명 NULL 질문 내용 수업이 어떤지 물어보는 내용",
                ),
                InputOutputTextPair(
                    input_text="과제 어떻고 수업 어때?에서 과목명, 교수명, 질문 내용이 뭐야?",
                    output_text="질문 내용 과제가 어떻고 수업이 어떤지 물어보는 내용",
                ),
                InputOutputTextPair(
                    input_text="강의평과 관련 없는 질문",
                    output_text="NULL",
                ),
            ],
            temperature=0.0,
            max_output_tokens=1024,
            top_p=0.8,
            top_k=1
        )

        #LLM에게 질문해서 user의 input으로부터 과목, 교수명 가져오기
        key_query = chat.send_message(question+"에서 과목명, 교수명, 질문 내용이 뭐야?").text

        if key_query == "NULL" :
            print("강의평과 관련된 내용을 입력하세요.")
            return

        lec, prof, query = extract(key_query)
        inputs = tokenizer(query, padding=True, truncation=True, return_tensors="pt")

        embeddings, _ = model(**inputs, return_dict=False)
        embedding_arr = embeddings[0][0].detach().numpy()
        embedding_str = ",".join(str(x) for x in embedding_arr)
        embedding_str = "["+embedding_str+"]"

        return lec, prof, embedding_str

        @staticmethod
        def extract(q): #LLM의 output으로부터 prof name, lecture name 추출
            lec = q.find("과목명")
            prof = q.find("교수명")
            q_start = q.find("질문 내용")

            lecture = q[lec+4:prof-1]
            professor = q[prof+4:]
            query = q[q_start+6:]
            if lecture == "NULL" : lecture = None
            if professor == "NULL" : professor = None
            return lecture, professor, query

    def chat(self, query_text, history):
        chat_model = ChatModel.from_pretrained("chat-bison@001")

        output_chat = chat_model.start_chat(
            context="강의를 찾는 대학생들에게 강의평들을 토대로 수업이 어떤지 알려주는 서비스야, 주어진 강의평들을 요약해서 학생들에게 알려줘" + articles + "강의평을 가져올 때는 있는 그대로 가져오지 말고 나름대로 요약해서 알려주고 공손하게 알려줘",
            message_history = history,
            temperature=0.3,
            max_output_tokens=1024,
            top_p=0.8,
            top_k=10
        )

        output = output_chat.send_message(query_text).text

        history.append(ChatMessage(content = query_text, author = "user"))
        history.append(ChatMessage(content = output, author = "bot"))

