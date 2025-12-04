import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="recruit_AI"
)

if db.is_connected():
    print("db connected successfully")

