import pg8000
from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy

class db_connect:
    def __init__(self, instance, user, password, name):
        self.instance_connection_name = instance
        self.db_user = user
        self.db_pass = password
        self.db_name = name
        self.pool = None

    def connect(self):
        connector = Connector()

        def getconn() -> pg8000.dbapi.Connection:
            conn: pg8000.dbapi.Connection = connector.connect(
                self.instance_connection_name,
                "pg8000",
                user=self.db_user,
                password=self.db_pass,
                db=self.db_name,
                ip_type=IPTypes.PUBLIC,
            )
            return conn

        self.pool = sqlalchemy.create_engine(
            "postgresql+pg8000://",
            creator=getconn,
            )

        with self.pool.connect() as db_conn:
            db_conn.execute(
            sqlalchemy.text(
                "CREATE EXTENSION IF NOT EXISTS vector with schema public"
            )
        )
        db_conn.commit()


    def query(self, lec, prof, q):
        if lec != None and prof != None :    #User의 질문 유형에 맞게 쿼리문 짜줌
            insert_stat, param = (sqlalchemy.text(
                        """SELECT origin_text, rating, assignment, team, grade, attendance, test FROM PROFNLEC WHERE INFO LIKE :information
                        ORDER BY v <-> :query_vec LIMIT 20"""   # <-> : L2 Distance,  <=> : Cosine Distance, <#> : inner product (음수 값을 return)
            ), {"information": f'%{lec}%{prof}%', "query_vec": q})
        elif lec != None :
            insert_stat, param = sqlalchemy.text(
                        """SELECT origin_text, rating, assignment, team, grade, attendance, test FROM PROFNLEC WHERE INFO LIKE :lecture
                        ORDER BY v <-> :query_vec LIMIT 20"""
            ), {"lecture": f'%{lec}%', "query_vec": q}
        elif prof != None :
            insert_stat, param = sqlalchemy.text(
                        """SELECT origin_text, rating, assignment, team, grade, attendance, test FROM PROFNLEC WHERE INFO LIKE :professor
                        ORDER BY v <-> :query_vec LIMIT 20"""
            ), {"professor": f'%{prof}%', "query_vec": q}

        with self.pool.connect() as db_conn: # 쿼리 실행문
            result = db_conn.execute(
                insert_stat, parameters = param
            ).fetchall()

        #query 결과를 문자열로 바꾸기 <- Context에는 문자열만 들어갈 수 있음
        articles = ""
        for res in result :
            articles += res[0]

        return articles