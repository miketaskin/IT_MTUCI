import psycopg2

conn = psycopg2.connect(database='postgres',
                        user='postgres',
                        password='root',
                        host="localhost",
                        port="5432")
cur = conn.cursor()

table_name = 'raspisanie'

cur.execute("SELECT * FROM raspisanie WHERE id > 6 AND id < 13;")
