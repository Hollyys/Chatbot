<<<<<<< HEAD
path = 'C:/Users/wjdfo/OneDrive/바탕 화면/project/final_output.json'

import pg8000
from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy
from transformers import AutoModel, AutoTokenizer

def get_KoSimCSE():
    model = AutoModel.from_pretrained('BM-K/KoSimCSE-roberta-multitask')
    tokenizer = AutoTokenizer.from_pretrained('BM-K/KoSimCSE-roberta-multitask')

    return model, tokenizer

model, tokenizer = get_KoSimCSE()

instance_connection_name = "esoteric-stream-399606:asia-northeast3:wjdfoek3"
db_user = "postgres" # @param {type:"string"}
db_pass = "pgvectorwjdfo" # @param {type:"string"}
db_name = "pgvector" # @param {type:"string"}

# initialize Cloud SQL Python Connector object
connector = Connector()

def getconn() -> pg8000.dbapi.Connection:
    conn: pg8000.dbapi.Connection = connector.connect(
        instance_connection_name,
        "pg8000",
        user=db_user,
        password=db_pass,
        db=db_name,
        ip_type=IPTypes.PUBLIC,
    )
    return conn

pool = sqlalchemy.create_engine(
    "postgresql+pg8000://",
    creator=getconn,
)

with pool.connect() as db_conn:
    db_conn.execute(
    sqlalchemy.text(
        "CREATE EXTENSION IF NOT EXISTS vector with schema public"
    )
    )
    db_conn.commit()

# pool.connect()하고 한 transaction만 수행 가능함.
# transaction 하나 수행하고 commit, close 하고 다시 connect 하기

import json
with pool.connect() as db_conn:
    db_conn.execute(
    sqlalchemy.text(
        "CREATE EXTENSION IF NOT EXISTS pg_trgm with schema public"
    )
    )
    db_conn.commit()
with pool.connect() as db_conn:
    try :
        db_conn.execute(
            sqlalchemy.text("drop table PROFNLEC")
        )
        db_conn.commit()
    except :
        print("table \'PROFNLEC\' does not exist")

with pool.connect() as db_conn:    #이미 table 존재하는 경우 제외
    db_conn.execute(
    sqlalchemy.text(
        """
        CREATE TABLE PROFNLEC(
            info varchar(50),
            info_num int,
            rating float,
            assignment varchar(50),
            team varchar(50),
            grade varchar(50),
            attendance varchar(50),
            test varchar(20),
            origin_text varchar(4096),
            v vector(768),
            PRIMARY KEY(info, info_num)
        )
        """
    )
    )
    db_conn.commit()

data = json.load(open(path, 'r', encoding = 'utf-8'))

with pool.connect() as db_conn:
    i = 1
    for key in data.keys():
        if data[key]['rating'] != 'NULL' :
            rating = data[key]['rating'].split()
            rating = rating[0]
        else : rating = data[key]['rating']
        if data[key]['assignment'] != 'NULL' : assignment = data[key]['assignment']
        else : assignment = data[key]['assignment']
        if data[key]['team_project'] != 'NULL' : team = data[key]['team_project']
        else : team = data[key]['team_project']
        if data[key]['grade'] != 'NULL' : grade = data[key]['grade']
        else : grade = data[key]['grade']
        if data[key]['attendence'] != 'NULL' : attendance = data[key]['attendence']
        else : attendance = data[key]['attendence']
        if data[key]['test_count'] != 'NULL' : test = data[key]['test_count']
        else : test = data[key]['test_count']


        for rep in data[key]['articles'] :
            rep = rep[rep.find('신고')+2:]
            print(rep)
            inputs = tokenizer(rep, padding = True, truncation = True, return_tensors = "pt")

            embeddings, _ = model(**inputs, return_dict = False)
            embedding_arr = embeddings[0][0].detach().numpy()
            embedding_str = ",".join(str(x) for x in embedding_arr)
            embedding_str = "["+embedding_str+"]"

            insert_stmt = sqlalchemy.text(
                "INSERT INTO PROFNLEC VALUES (:info, :info_num, :rating, :assignment, :team, :grade, :attendance, :test, :origin_text, :v)"
            )

            db_conn.execute(
                insert_stmt, parameters={"info": key,"info_num": i, "rating": rating, "assignment": assignment, "team":team,
                                        "grade": grade, "attendance": attendance, "test": test,
                                        "origin_text": rep, 'v': embedding_str}
            )
            print("%s, insert %d-tuple clear" %(key, i))
            i+=1

    db_conn.commit()
db_conn.close()
=======
path = 'C:/Users/wjdfo/OneDrive/바탕 화면/project/final_output.json'

import pg8000
from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy
from transformers import AutoModel, AutoTokenizer

def get_KoSimCSE():
    model = AutoModel.from_pretrained('BM-K/KoSimCSE-roberta-multitask')
    tokenizer = AutoTokenizer.from_pretrained('BM-K/KoSimCSE-roberta-multitask')

    return model, tokenizer

model, tokenizer = get_KoSimCSE()

instance_connection_name = "esoteric-stream-399606:asia-northeast3:wjdfoek3"
db_user = "postgres" # @param {type:"string"}
db_pass = "pgvectorwjdfo" # @param {type:"string"}
db_name = "pgvector" # @param {type:"string"}

# initialize Cloud SQL Python Connector object
connector = Connector()

def getconn() -> pg8000.dbapi.Connection:
    conn: pg8000.dbapi.Connection = connector.connect(
        instance_connection_name,
        "pg8000",
        user=db_user,
        password=db_pass,
        db=db_name,
        ip_type=IPTypes.PUBLIC,
    )
    return conn

pool = sqlalchemy.create_engine(
    "postgresql+pg8000://",
    creator=getconn,
)

with pool.connect() as db_conn:
    db_conn.execute(
    sqlalchemy.text(
        "CREATE EXTENSION IF NOT EXISTS vector with schema public"
    )
    )
    db_conn.commit()

# pool.connect()하고 한 transaction만 수행 가능함.
# transaction 하나 수행하고 commit, close 하고 다시 connect 하기

import json
with pool.connect() as db_conn:
    db_conn.execute(
    sqlalchemy.text(
        "CREATE EXTENSION IF NOT EXISTS pg_trgm with schema public"
    )
    )
    db_conn.commit()
with pool.connect() as db_conn:
    try :
        db_conn.execute(
            sqlalchemy.text("drop table PROFNLEC")
        )
        db_conn.commit()
    except :
        print("table \'PROFNLEC\' does not exist")

with pool.connect() as db_conn:    #이미 table 존재하는 경우 제외
    db_conn.execute(
    sqlalchemy.text(
        """
        CREATE TABLE PROFNLEC(
            info varchar(50),
            info_num int,
            rating float,
            assignment varchar(50),
            team varchar(50),
            grade varchar(50),
            attendance varchar(50),
            test varchar(20),
            origin_text varchar(4096),
            v vector(768),
            PRIMARY KEY(info, info_num)
        )
        """
    )
    )
    db_conn.commit()

data = json.load(open(path, 'r', encoding = 'utf-8'))

with pool.connect() as db_conn:
    i = 1
    for key in data.keys():
        if data[key]['rating'] != 'NULL' :
            rating = data[key]['rating'].split()
            rating = rating[0]
        else : rating = data[key]['rating']
        if data[key]['assignment'] != 'NULL' : assignment = data[key]['assignment']
        else : assignment = data[key]['assignment']
        if data[key]['team_project'] != 'NULL' : team = data[key]['team_project']
        else : team = data[key]['team_project']
        if data[key]['grade'] != 'NULL' : grade = data[key]['grade']
        else : grade = data[key]['grade']
        if data[key]['attendence'] != 'NULL' : attendance = data[key]['attendence']
        else : attendance = data[key]['attendence']
        if data[key]['test_count'] != 'NULL' : test = data[key]['test_count']
        else : test = data[key]['test_count']


        for rep in data[key]['articles'] :
            rep = rep[rep.find('신고')+2:]
            print(rep)
            inputs = tokenizer(rep, padding = True, truncation = True, return_tensors = "pt")

            embeddings, _ = model(**inputs, return_dict = False)
            embedding_arr = embeddings[0][0].detach().numpy()
            embedding_str = ",".join(str(x) for x in embedding_arr)
            embedding_str = "["+embedding_str+"]"

            insert_stmt = sqlalchemy.text(
                "INSERT INTO PROFNLEC VALUES (:info, :info_num, :rating, :assignment, :team, :grade, :attendance, :test, :origin_text, :v)"
            )

            db_conn.execute(
                insert_stmt, parameters={"info": key,"info_num": i, "rating": rating, "assignment": assignment, "team":team,
                                        "grade": grade, "attendance": attendance, "test": test,
                                        "origin_text": rep, 'v': embedding_str}
            )
            print("%s, insert %d-tuple clear" %(key, i))
            i+=1

    db_conn.commit()
db_conn.close()
>>>>>>> d8fd5352b185ee0ddd94b238addbb03fd56b0047
