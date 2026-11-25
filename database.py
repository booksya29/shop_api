import psycopg2


def connect_db():
     conn = psycopg2.connect(
            user = "postgres",
            password = "1234",
            host = "localhost",
            port = "5432",
            dbname = "shop"
        )
     return conn