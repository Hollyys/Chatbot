import pg8000
from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy

instance_connection_name = "esoteric-stream-399606:asia-northeast3:wjdfoek3"
db_user = "postgres"
db_pass = "pgvectorwjdfo"
db_name = "pgvector"

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