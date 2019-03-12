import pyodbc
import psycopg2
import hashlib, uuid

#-------------------------------------------------
# Helper Functions
#-------------------------------------------------
def create_table1(cursor):
    cursor.execute("CREATE TABLE all_user_info (Username varchar, Password varchar, FirstName varchar, LastName varchar, PhoneNumber varchar, EmailAddress varchar, Company varchar, Gender varchar);")

def create_table2(cursor):
    cursor.execute("CREATE TABLE user_info (FirstName varchar, LastName varchar, PhoneNumber varchar, EmailAddress varchar, Company varchar, Gender varchar);")

def add_credentials(cursor,user):
    query = "INSERT INTO all_user_info (Username,Password)" \
            "VALUES ('" + user[0] + "','" + user[1] + "');"
    cursor.execute(query) 

def add_user_info(cursor,user,creds):
    query1 = "UPDATE all_user_info SET FirstName = '" + user[0] + "', LastName = '" + user[1] + "', PhoneNumber = '" + user[2] + "', EmailAddress = '" + user[3] + "', Company = '" + user[4] + "', Gender = '" + user[5] + "' WHERE Username = '" + creds[0] + "' AND Password = '" + creds[1] + "'"  
    query2 = "INSERT INTO user_info (FirstName,LastName,PhoneNumber,EmailAddress,Company,Gender)" \
             "VALUES ('" + user[0] + "','" + user[1] + "','" + user[2] + "','" + user[3] + "','" + user[4] + "','" + user[5] + "');"   
    cursor.execute(query1)
    cursor.execute(query2)
 
def check_login(creds,cursor):
    cursor.execute("SELECT * FROM all_user_info")
    tables = cursor.fetchall()
    for row in tables:
        row_tuple = tuple(row)
        if(row_tuple[0] == creds[0] and row_tuple[1] == creds[1]):
            return True
    return False

def check_valid_username(cursor,creds):
    cursor.execute("SELECT Username FROM all_user_info")
    usernames = cursor.fetchall()
    valid = True
    for username in usernames:
        user = username[0]
        if(creds[0] == user):
            valid = False
    return valid

def check_valid_password(password):
    lower_case = False
    upper_case = False
    number = False
    for i in password:
        if(i.islower()):
            lower_case = True
        elif(i.isupper()):
            upper_case = True
        elif(i.isdigit()):
            number = True
    return lower_case and upper_case and number

def check_valid_phone(user):
    return user[2].isdigit()

def check_valid_email(user):
    for i in user[3]:
        if(i == '@'):
            return True
    return False

def hash_password(password):
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha512(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()
    return hashed_password

#-------------------------------------------------
# Main Code
#-------------------------------------------------

# Connect to Database
conn = psycopg2.connect(dbname="database", user="postgres", password="password", host="11.111.111.11", port="5432")   
cursor = conn.cursor()

# Create Tables
#create_table1(cursor)
#create_table2(cursor)

# Create user info
user = ("Markus","Paal","9058345983","biokio@acm.com","Amazon","Male")
username = "MarkP"
password = "qwertY1234"

# Validate password and hash it in order to store it into the database
check_valid_password(password)
hashed_password = hash_password(password)
creds = (username,hashed_password)

# Validate user information
if(check_valid_username(cursor,creds)):
    if(check_valid_phone(user)):
        if(check_valid_email(user)): 
            add_credentials(cursor,creds)
            validate = check_login(creds,cursor)
            print(validate)
            add_user_info(cursor,user,creds)
        else:
           print("Invalid email") 
    else:
        print("Invalid Phone Number")
else:
    print("Username already exists")

# Print the whole table
cursor.execute("SELECT * FROM all_user_info")
tables = cursor.fetchall()
print(tables)

conn.commit()
conn.close()
cursor.close()
