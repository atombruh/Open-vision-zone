import mysql.connector


my = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="nirupan@123"

)
my_cursor = my.cursor()

#my_cursor.execute("CREATE DATABASE students")

