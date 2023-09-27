import pymysql

mydb = pymysql.connect(
    host="localhost",x
    user="database username",
    password="database password",
    database="watchscope"
)

# create a table named "programs"
mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE programs (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), Asset_Identifier VARCHAR(1000), type VARCHAR(255), platform VARCHAR(255))")
mydb.commit()
mydb.close()
