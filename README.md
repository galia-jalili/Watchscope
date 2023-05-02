# Watchscope

### A program to receive the latest changes in the scopes of the programs on hackerone, bugcrowd, and yeswehack.

#### 1- Create a database according to the ```mysql.py``` file.
#### 2- Edit the ```mysql.py``` file and enter your database information, then run mysql.py to create the desired table.
```python3 mysql.py```
#### 3- Edit ```watchscope.py``` and write your databases information and webhook links and then run file.
```python
def connect_to_mysql():
    try:
        # connect to the database
        db = mysql.connector.connect(
            host="localhost",
            user="database username",
            password="database password",
            database="watchscope"
        )

        # return the database connection object
        return db
```        
```python
discord_webhook_url = "your webhook link"
discord_webhook_url_error = "your webhook link for error messages"
```
### Note: Before making changes to your code, you should create two channels in your Discord server: one for receiving new scopes and another for receiving potential errors, so that you can use their webhook URLs in your code.

#### in this code we use https://github.com/Osb0rn3/bugbounty-targets repository.
