import os
import mysql.connector

from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_DB = os.getenv('DB_DB')

def conexao_banco():
     return mysql.connector.connect(
    host =DB_HOST,
    user =DB_USER,
    password =DB_PASSWORD,
    database =DB_DB,
    )