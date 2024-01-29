import psycopg2
conn = psycopg2.connect(database="flask_db", host="localhost",user="postgres", password="postgres",port="5432")
cur=conn.cursor()
cur.execute('''create table if not exists courses (id serial primary key, name varchar(100), fees integer, duration integer);''')
cur.execute('''insert into courses(name,fees,duration) values('python',6500,44),('java',50000,'55'),('c',54444,45)''')
conn.commit()
cur.close()
