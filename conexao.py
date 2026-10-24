import psycopg

def conectar():
    return psycopg.connect(
        dbname="escola",
        user="postgres",
        password="94791166",
        host="localhost",
        port=5432
    )

