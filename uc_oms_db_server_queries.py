from uc_oms_db_funcs import assembleSQLFields

def query_selectUserByUsername(db_connection, user: str): # Gets user_id of username
    table = 'uc_users'
    field = 'user_id'
    condition = "username='{}'".format(user)
    sql = "SELECT {} FROM {} WHERE {}".format(field, table, condition)
    mycursor = db_connection.cursor()
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult

def query_selectUsernameAndPasswordByUsername(db_connection, user: str): # Gets username and password of username
    table = 'uc_users'
    fields = ['username','password']
    fields = assembleSQLFields(fields)
    condition = "username='{}'".format(user)
    sql = "SELECT {} FROM {} WHERE {}".format(fields, table, condition)
    mycursor = db_connection.cursor()
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult

def query_insertNewUser(db_connection, user: str, hashed: str): # Inserts new entry into uc_users
    table = 'uc_users'
    fields = ['username','password']
    fields = assembleSQLFields(fields)
    values = "'{}','{}'".format(user, hashed)
    sql = "INSERT INTO {} ({}) VALUES ({})".format(table, fields, values)
    mycursor = db_connection.cursor()
    mycursor.execute(sql)
    db_connection.commit()