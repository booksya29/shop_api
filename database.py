import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


def connect_db():
     conn = psycopg2.connect(
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD"),
            host = os.getenv("DB_HOST"),
            port = os.getenv("DB_PORT"),
            dbname = os.getenv("DB_NAME")
        )
     return conn


def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY, name TEXT, born_year INTEGER, budget NUMERIC)")
    cursor.execute("CREATE TABLE IF NOT EXISTS products(id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY, barcode TEXT UNIQUE, user_id INTEGER, name TEXT, price NUMERIC, count INTEGER, description TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS transactions(id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY, buyer_id INTEGER, product_barcode TEXT, price NUMERIC, b_change NUMERIC, count INTEGER, date DOUBLE PRECISION)")
    conn.commit()
    cursor.close()

