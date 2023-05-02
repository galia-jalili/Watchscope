
mydb = mysql.connector.connect(
    host="localhost",
    user="database username",
    password="database password",
    database="watchscope"
)

# create a table named "programs"
mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE programs (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), asset_identifier VARCHAR(255, type VARCHAR(255), platform VARCHAR(255))")


mydb.commit()
mydb.close()
