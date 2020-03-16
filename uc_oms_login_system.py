from passlib.context import CryptContext
import secrets

class OMSUser():
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.token = ''
        self.authenticated = False

def assembleSQLFields(fields): # Translates fields list to sql string
  fieldsString =""
  for x in fields:
    if fieldsString == "":
        fieldsString = x
    else:
        stingFormat = "{}, {}"
        fieldsString = stingFormat.format(fieldsString,x)
  return fieldsString

def query_selectUserByUsername(db_connection, user): # Gets user_id of username
    table = 'uc_users'
    field = 'user_id'
    condition = "username='{}'".format(user)
    sql = "SELECT {} FROM {} WHERE {}".format(field, table, condition)
    mycursor = db_connection.cursor()
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult

def query_selectUsernameAndPasswordByUsername(db_connection, user): # Gets username and password of username
    table = 'uc_users'
    fields = ['username','password']
    fields = assembleSQLFields(fields)
    condition = "username='{}'".format(user)
    sql = "SELECT {} FROM {} WHERE {}".format(fields, table, condition)
    mycursor = db_connection.cursor()
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult

def query_insertNewUser(db_connection, user, hashed): # Inserts new entry into uc_users
    table = 'uc_users'
    fields = ['username','password']
    fields = assembleSQLFields(fields)
    values = "'{}','{}'".format(user, hashed)
    sql = "INSERT INTO {} ({}) VALUES ({})".format(table, fields, values)
    mycursor = db_connection.cursor()
    mycursor.execute(sql)
    db_connection.commit()

class LoginInterface(object): # Creates login interface object
    def __init__(self): # Defines variables when instantiated
        self.pwd_context = CryptContext(
            schemes=["pbkdf2_sha256"],
            default="pbkdf2_sha256",
            pbkdf2_sha256__default_rounds=30000
            )
        self.user = ''
        self.authenticated = False

    def newUser(self, user, password): # Adds new user to database
        db_connection = loginDBConnect()
        check_result = query_selectUserByUsername(db_connection, user)
        if len(check_result) == 0:
            hashed = self.encryptPassword(password)
            query_insertNewUser(db_connection, user, hashed)
            print('New User Added')
        else:
            print('Failed to Add New User')

    def login(self, user, password): # Authenticates user
        db_connection = loginDBConnect()
        result = query_selectUsernameAndPasswordByUsername(db_connection, user)
        self.authenticated = False
        self.user = ''
        code = 0
        if len(result) == 1:
            password_result = result[0][1]
            if self.checkEncryptedPassword(password, password_result):
                self.authenticated = True
                self.user = user
                code = 1
            else:
                self.authenticated = False
                self.user = ''
                code = 2
        elif len(result) == 0:
            self.authenticated = False
            self.user = ''
            code = 3
        else:
            self.authenticated == False
            self.user = ''
            code = 4
        return code

    def logout(self): # Logs out user
        self.authenticated = False
        self.user = ''

    def encryptPassword(self, password): # Encrypts password
        return self.pwd_context.encrypt(password)

    def checkEncryptedPassword(self, password, hashed): # Checks if password matches hashed
        return self.pwd_context.verify(password, hashed)