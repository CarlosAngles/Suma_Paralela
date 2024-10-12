import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="suma_paralela"
)
cursor = db.cursor()
for _ in range(1000000):
    cursor.execute("INSERT INTO datos (valor) VALUES (1)")
    
db.commit()
cursor.close()
db.close()
