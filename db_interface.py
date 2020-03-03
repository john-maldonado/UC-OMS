import mysql.connector
from tabulate import tabulate
import time
import datetime

def db_connect():
  connection = mysql.connector.connect(
    host="10.0.0.119",
    user="uc_orders",
    passwd="-dJS+2!mFRexjbP?",
    database="uc_db"
  )
  return connection

def query_basic(db_connection):
  table = "sales_orders"
  fields = ['so_id', 'entered_ts', 'so_number', 'description', 'customer', 'order_date', 'closed']
  fieldsString = assembleSQLFields(fields)
  sql = "SELECT {} FROM {}"
  sql = sql.format(fieldsString, table)
  mycursor = db_connection.cursor()
  mycursor.execute(sql)
  myresult = mycursor.fetchall()
  print(tabulate(myresult, headers=fields, tablefmt='psql'))

def query_all(db_connection):
  table = "sales_orders"
  fields = ['so_id', 'entered_ts', 'so_number', 'description', 'customer', 'order_date', 'due_date', 'quote_number', 'customer_po', 'completed_date', 'completed', 'invoiced', 'invoice_number', 'invoice_date', 'invoice_amount', 'paid_full', 'paid_date', 'paid_amount', 'closed']
  fieldsString = assembleSQLFields(fields)
  sql = "SELECT {} FROM {}"
  sql = sql.format(fieldsString, table)
  mycursor = db_connection.cursor()
  mycursor.execute(sql)
  myresult = mycursor.fetchall()
  print(tabulate(myresult, headers=fields, tablefmt='psql'))

def query_allopen(db_connection):
  table = "sales_orders"
  fields = ['so_id', 'so_number', 'description', 'customer', 'order_date','due_date', 'completed', 'invoiced', 'invoice_amount', 'paid_amount', 'paid_full']
  fieldsString = assembleSQLFields(fields)
  condition = "closed = 0"
  mycursor = db_connection.cursor()
  sql = "SELECT {} FROM {} WHERE {}"
  sql = sql.format(fieldsString, table, condition)
  mycursor.execute(sql)
  myresult = mycursor.fetchall()
  return myresult, fields

def query_insertIntoTimeLog(db_connection, SalesOrder):
  SalesOrderString = "{}".format(SalesOrder)
  TimeStamp = "{}".format(time.strftime('%Y-%m-%d %H:%M:%S'))
  table = "time_log"
  fields = ['so_number', 'clockin_ts']
  fieldsString = assembleSQLFields(fields)
  values = "'{}', '{}'"
  values = values.format(SalesOrderString,TimeStamp)
  sql = "INSERT INTO {} ({}) VALUES ({})"
  sql = sql.format(table, fieldsString, values)
  mycursor = db_connection.cursor()
  mycursor.execute(sql)
  db_connection.commit()

def query_timeLogBySO(db_connection, SalesOrder):
  SalesOrderString = "{}".format(SalesOrder)
  table = "time_log"
  fields = ['log_id', 'so_number', 'clockin_ts', 'clockout_ts', 'activity']
  fieldsString = assembleSQLFields(fields)
  condition = "so_number='{}'"
  condition = condition.format(SalesOrderString)
  sql = "SELECT {} FROM {} WHERE {}"
  sql = sql.format(fieldsString, table, condition)
  mycursor = db_connection.cursor()
  mycursor.execute(sql)
  myresult = mycursor.fetchall()
  # print(tabulate(myresult, headers=fields, tablefmt='psql'))
  return myresult, fields

def query_updateTimeLogClockOut(db_connection, logID, activity):
  TimeStamp = "{}".format(time.strftime('%Y-%m-%d %H:%M:%S'))
  ActivityString = "{}".format(activity)
  sql = "UPDATE time_log SET clockout_ts='{}', activity='{}' WHERE log_id={}"
  sql = sql.format(TimeStamp,ActivityString,logID)
  mycursor = db_connection.cursor()
  mycursor.execute(sql)
  db_connection.commit()

def query_timeLogTotalTimeBySO(db_connection, SalesOrder):
  SalesOrderString = "{}".format(SalesOrder)
  table = "time_log"
  fields = ['log_id', 'so_number', 'clockin_ts', 'clockout_ts', 'activity']
  fieldsString = assembleSQLFields(fields)
  condition = "so_number='{}'"
  condition = condition.format(SalesOrderString)
  sql = "SELECT {} FROM {} WHERE {}"
  sql = sql.format(fieldsString, table, condition)
  mycursor = db_connection.cursor()
  mycursor.execute(sql)
  myresult = mycursor.fetchall()
  tabulatedResult = tabulate(myresult, headers=fields, tablefmt='psql')
  print(tabulatedResult)
  totalTime = datetime.timedelta(0)
  for result in myresult:
   lineTime = result[3]-result[2]
   totalTime = totalTime + lineTime
  totalTimeSeconds = totalTime.total_seconds()
  totalTimeHours = round((totalTimeSeconds/60)/60,2)
  return totalTimeHours

def query_timeLogByLogID(db_connection, logID):
  table = "time_log"
  fields = ['log_id', 'so_number', 'clockin_ts', 'clockout_ts', 'activity']
  fieldsString = assembleSQLFields(fields)
  condition = "log_id='{}'"
  condition = condition.format(logID)
  sql = "SELECT {} FROM {} WHERE {}"
  sql = sql.format(fieldsString, table, condition)
  mycursor = db_connection.cursor()
  mycursor.execute(sql)
  myresult = mycursor.fetchall()
  return myresult, fields

def query_deleteTimeLogByLogID(db_connection, logID):
  table = "time_log"
  condition = "log_id='{}'"
  condition = condition.format(logID)
  sql = "DELETE FROM {} WHERE {}"
  sql = sql.format(table, condition)
  mycursor = db_connection.cursor()
  mycursor.execute(sql)
  db_connection.commit()

def query_salesOrderBySONumber(db_connection, SalesOrder):
  SalesOrderString = "{}".format(SalesOrder)
  table = "sales_orders"
  fields = ['so_id', 'entered_ts', 'so_number', 'description', 'customer', 'order_date', 'due_date', 'quote_number', 'customer_po', 'completed_date', 'completed', 'invoiced', 'invoice_number', 'invoice_date', 'invoice_amount', 'paid_full', 'paid_date', 'paid_amount', 'closed']
  fieldsString = assembleSQLFields(fields)
  condition = "so_number='{}'"
  condition = condition.format(SalesOrderString)
  sql = "SELECT {} FROM {} WHERE {}"
  sql = sql.format(fieldsString, table, condition)
  mycursor = db_connection.cursor()
  mycursor.execute(sql)
  myresult = mycursor.fetchall()
  print("---------------------------------------")
  print("Search results for: {}".format(SalesOrderString))
  print("---------------------------------------")
  for x in myresult:
    for i in range(len(x)):
      field = fields[i]
      value = x[i]
      printString ="{} = {}".format(field, value)
      print(printString)
    print("---------------------------------------")

def query_salesOrderBySONumberShort(db_connection, SalesOrder):
  SalesOrderString = "{}".format(SalesOrder)
  table = "sales_orders"
  fields = ['so_number', 'description', 'customer', 'order_date', 'due_date', 'quote_number', 'customer_po', 'completed_date', 'completed', 'invoiced', 'invoice_number', 'invoice_date', 'invoice_amount', 'paid_full', 'paid_date', 'paid_amount', 'closed']
  fieldsString = assembleSQLFields(fields)
  condition = "so_number='{}'"
  condition = condition.format(SalesOrderString)
  sql = "SELECT {} FROM {} WHERE {}"
  sql = sql.format(fieldsString, table, condition)
  mycursor = db_connection.cursor()
  mycursor.execute(sql)
  myresult = mycursor.fetchall()
  return myresult

def query_salesOrderByCustomer(db_connection, Customer):
  CustomerString = "{}".format(Customer)
  table = "sales_orders"
  fields = ['so_id', 'entered_ts', 'so_number', 'description', 'customer', 'order_date', 'due_date', 'quote_number', 'customer_po', 'completed_date', 'completed', 'invoiced', 'invoice_number', 'invoice_date', 'invoice_amount', 'paid_full', 'paid_date', 'paid_amount', 'closed']
  fieldsString = assembleSQLFields(fields)
  condition = "customer='{}'"
  condition = condition.format(CustomerString)
  sql = "SELECT {} FROM {} WHERE {}"
  sql = sql.format(fieldsString, table, condition)
  mycursor = db_connection.cursor()
  mycursor.execute(sql)
  myresult = mycursor.fetchall()
  print("---------------------------------------")
  print("Search results for: {}".format(CustomerString))
  print("---------------------------------------")
  for x in myresult:
    for i in range(len(x)):
      field = fields[i]
      value = x[i]
      printString ="{} = {}".format(field, value)
      print(printString)
    print("---------------------------------------")

def query_maxSalesOrder(db_connection):
  table = "sales_orders"
  field = "so_number"
  sql = "SELECT MAX({}) FROM {}"
  sql = sql.format(field, table)
  db_connection = db_connect()
  mycursor = db_connection.cursor()
  mycursor.execute(sql)
  myresult = mycursor.fetchall()
  return myresult[0][0]

def query_insertIntoSalesOrders(db_connection,salesOrder, description, customer, orderDate, dueDate):
  table = "sales_orders"
  fields = ['so_number', 'description', 'customer', 'order_date', 'due_date']
  fieldsString = assembleSQLFields(fields)
  values = "'{}', '{}', '{}', '{}', '{}'"
  values = values.format(salesOrder, description, customer, orderDate, dueDate)
  sql = "INSERT INTO {} ({}) VALUES ({})"
  sql = sql.format(table,fieldsString,values)
  mycursor = db_connection.cursor()
  mycursor.execute(sql)
  db_connection.commit()

def query_updateSalesOrderSingleField(db_connection, salesOrder, field, value):
  table = "sales_orders"
  condition = "so_number='{}'"
  condition = condition.format(salesOrder)
  sql = "UPDATE {} SET {}='{}' WHERE {}"
  sql = sql.format(table,field,value,condition)
  mycursor = db_connection.cursor()
  mycursor.execute(sql)
  db_connection.commit()

def query_updateSalesOrderMultipleFields(db_connection, salesOrder, fields, values):
  table = "sales_orders"
  condition = "so_number='{}'"
  condition = condition.format(salesOrder)
  fieldsAndValues = ""
  if len(fields) == len(values):
    fieldsAndValues = ""
    for i in range(len(fields)):
        fieldAndValue = "{}='{}'"
        fieldAndValue = fieldAndValue.format(fields[i],values[i])
        if (len(fieldsAndValues) == 0):
            appendString = fieldAndValue
        else:
            appendString = ", {}"
            appendString = appendString.format(fieldAndValue)
        fieldsAndValues = fieldsAndValues + appendString
    sql = "UPDATE {} SET {} WHERE {}"
    sql = sql.format(table, fieldsAndValues, condition)
    mycursor = db_connection.cursor()
    mycursor.execute(sql)
    db_connection.commit()

def query_updateTimeLogSingleField(db_connection, logID, field, value):
  table = "time_log"
  condition = "log_id='{}'"
  condition = condition.format(logID)
  sql = "UPDATE {} SET {}='{}' WHERE {}"
  sql = sql.format(table,field,value,condition)
  mycursor = db_connection.cursor()
  mycursor.execute(sql)
  db_connection.commit()

def assembleSQLFields(fields):
  fieldsString =""
  for x in fields:
    if fieldsString == "":
        fieldsString = x
    else:
        stingFormat = "{}, {}"
        fieldsString = stingFormat.format(fieldsString,x)
  return fieldsString

def translateSalesOrdersResults(results, fields):
  for i in range(len(results)):
    row = results[i]
    row = list(row)
    for j in range(len(row)):
      field = fields[j]
      # Translate entered_ts
      if field == 'entered_ts':
        row[j] = row[j].strftime("%m/%d/%Y, %H:%M:%S")
      # Translate dates
      elif ((field == 'order_date') or (field == 'due_date') or (field == 'invoice_date') or (field == 'paid_date')):
        row[j] = row[j].strftime("%m/%d/%Y")
      # Translate booleans
      elif ((field == 'completed') or (field == 'invoiced') or (field == 'paid_full') or (field == 'closed')):
        if row[j] == 1:
          row[j] = 'Yes'
        else:
          row[j] = 'No'
      # Translate dollar amounts
      elif ((field == 'invoice_amount') or (field == 'paid_amount')):
        if not (row[j] == None):
          print(row[j])
          row[j] = '${:,.2f}'.format(row[j])
          print(row[j])
      # If translation not defined, pass original value
      else:
        row[j] = row[j]
    row = tuple(row)
    results[i] = row
  return results

def prettySalesOrderHeaders(fields):
  for i in range(len(fields)):
    field = fields[i]
    all_fields = ['so_id', 'entered_ts', 'so_number', 'description', 'customer', 'order_date', 'due_date', 'quote_number', 'customer_po', 'completed_date', 'completed', 'invoiced','invoice_number', 'invoice_date', 'invoice_amount', 'paid_full', 'paid_date', 'paid_amount', 'closed']
    all_pretty_headers = ['SO ID', 'Time Stamp', 'SO Number', 'Description', 'Customer', 'Order Date', 'Due Date', 'Quote Number', 'Customer PO', 'Completed Date', 'Completed', 'Invoiced', 'Invoice No', 'Invoice Date', 'Invoice Amount', 'Paid In Full', 'Paid Date', 'Paid Amount', 'Closed']
    if field in all_fields:
      index = all_fields.index(field)
      fields[i] = all_pretty_headers[index]
    else:
      fields[i] = field
  return fields