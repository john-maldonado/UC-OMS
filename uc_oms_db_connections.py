import mysql.connector

def loginDBConnect(): # Creates connection to uc_db with uc_login user
    connection = mysql.connector.connect(
    host="172.17.0.1",
    user="uc_login",
    passwd="^6h@fJV9BzzkKjBc",
    database="uc_db"
    )
    return connection

def ordersDBConnect():
  connection = mysql.connector.connect(
    host="172.17.0.1",
    user="uc_orders",
    passwd="-dJS+2!mFRexjbP?",
    database="uc_db"
  )
  return connection
