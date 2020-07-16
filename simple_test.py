#!/usr/bin/python3
import config

def checkName(name):
  checkName = input("Is your name " + name + "? ") 
  
  if checkName.lower() == "yes":    
    print("Hello,", name)  
  else:    
    name = input("We're sorry about that. What is your name again? ")    
    print("Welcome,", name)

checkName("Ethan")

#!/usr/bin/python
import MySQLdb

# Setup MySQL Connection
db = MySQLdb.connect(host="localhost", user="root", passwd=config.db_password, db="python")
cursor = db.cursor()

# Insert a row into our table
cursor.execute("INSERT INTO users (firstname) VALUES ('Ethan')")

# Save changes to database
db.commit()
