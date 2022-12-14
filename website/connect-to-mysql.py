import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Ee123456!!',
    port='3306',
    database='patient'
)

mycursor = mydb.cursor()

mycursor.execute('SELECT * FROM users')

users = mycursor.fetchall()

for user in users:
    print(user)
    print('email: ' + user[1])