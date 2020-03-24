import time
import datetime
import json
import socket
from uc_oms_protocol import Protocol, PCommands, PExceptions, OMSUser

def query_selectBasic(client_socket, user):
  table = "sales_orders"
  fields = ['so_id', 'entered_ts', 'so_number', 'description', 'customer', 'order_date', 'closed']
  fieldsString = assembleSQLFields(fields)
  sql = "SELECT {} FROM {}"
  sql = sql.format(fieldsString, table)
  results, exception = requestSelectQuery(client_socket, user, sql)
  return results, fields, exception

def query_selectAll(db_connection):
  table = "sales_orders"
  fields = ['so_id', 'entered_ts', 'so_number', 'description', 'customer', 'order_date', 'due_date', 'quote_number', 'customer_po', 'completed_date', 'completed', 'invoiced', 'invoice_number', 'invoice_date', 'invoice_amount', 'paid_full', 'paid_date', 'paid_amount', 'closed']
  fieldsString = assembleSQLFields(fields)
  sql = "SELECT {} FROM {}"
  sql = sql.format(fieldsString, table)
  mycursor = db_connection.cursor()
  mycursor.execute(sql)
  myresult = mycursor.fetchall()
  return myresult, fields

def query_selectAllOpen(client_socket, user):
  table = "sales_orders"
  fields = ['so_id', 'so_number', 'description', 'customer', 'order_date','due_date', 'completed', 'invoiced', 'invoice_amount', 'paid_amount', 'paid_full']
  fieldsString = assembleSQLFields(fields)
  condition = "closed = 0"
  sql = "SELECT {} FROM {} WHERE {}"
  sql = sql.format(fieldsString, table, condition)
  results, exception = requestSelectQuery(client_socket, user, sql)
  return results, fields, exception

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

def query_selectTimeLogBySO(db_connection, SalesOrder):
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

def query_selectTimeLogTotalTimeBySO(db_connection, SalesOrder):
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
  totalTime = datetime.timedelta(0)
  for result in myresult:
   lineTime = result[3]-result[2]
   totalTime = totalTime + lineTime
  totalTimeSeconds = totalTime.total_seconds()
  totalTimeHours = round((totalTimeSeconds/60)/60,2)
  return totalTimeHours

def query_selectTimeLogByLogID(db_connection, logID):
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

def query_selectSalesOrderBySONumber(db_connection, SalesOrder):
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
  return myresult, fields

def query_selectSalesOrderBySONumberShort(db_connection, SalesOrder):
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
  return myresult, fields

def query_selectSalesOrderByCustomer(db_connection, Customer):
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
  return myresult, fields

def query_selectMaxSalesOrder(client_socket: socket.socket, user: OMSUser):
  table = "sales_orders"
  field = "so_number"
  sql = "SELECT MAX({}) FROM {}"
  sql = sql.format(field, table)
  results, exception = requestSelectQuery(client_socket, user, sql)
  return results, field, exception

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

def assembleSQLFields(fields):
  fieldsString =""
  for x in fields:
    if fieldsString == "":
        fieldsString = x
    else:
        stingFormat = "{}, {}"
        fieldsString = stingFormat.format(fieldsString,x)
  return fieldsString

def translateResults(results, fields):
  for i in range(len(results)):
    row = results[i]
    row = list(row)
    for j in range(len(row)):
      if (not (row[j] == None)):
        field = fields[j]
        # Translate time stamps
        if ((field == 'entered_ts') or (field == 'clockin_ts') or (field == 'clockout_ts')):
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
            row[j] = '${:,.2f}'.format(row[j])
        # If translation not defined, pass original value
        else:
          row[j] = row[j]
    row = tuple(row)
    results[i] = row
  return results

class fieldsDictionary(object):
    def __init__(self):
        self.forward_dict = {
            'so_id': 'SO ID',
            'entered_ts': 'Time Stamp',
            'so_number': 'SO Number',
            'description': 'Description',
            'customer': 'Customer',
            'order_date': 'Order Date',
            'due_date': 'Due Date',
            'quote_number': 'Quote Number',
            'customer_po': 'Customer PO',
            'completed_date': 'Completed Date',
            'completed': 'Completed',
            'invoiced': 'Invoiced',
            'invoice_number': 'Invoice No',
            'invoice_date': 'Invoice Date',
            'invoice_amount': 'Invoice Amount',
            'paid_full': 'Paid In Full',
            'paid_date': 'Paid Date',
            'paid_amount': 'Paid Amount',
            'closed': 'Closed',
            'log_id': 'Log ID',
            'clockin_ts': 'Clock In',
            'clockout_ts': 'Clock Out',
            'activity': 'Activity'
            }
        self.reverse_dict = self.reverseDict(self.forward_dict)
    
    def reverseDict(self, forward_dict):
        return dict(zip(forward_dict.values(), forward_dict.keys()))

    def fieldToHeader(self, field):
        return self.forward_dict.get(field)
    
    def headerToField(self, header):
        return self.reverse_dict.get(header)
        
def prettyHeaders(fields_input: list):
  fields_dict = fieldsDictionary()
  headers = []
  for x in fields_input:
      if x in fields_dict.forward_dict:
          headers.append(fields_dict.fieldToHeader(x))
      else:
          headers.append(x)
  return headers

def requestSelectQuery(client_socket, user, query_string):
  p = Protocol()
  p.sendQuery(client_socket,PCommands.select_query, user, query_string)
  client_socket.setblocking(True)
  message = p.receiveMessage(client_socket)
  client_socket.setblocking(False)
  if message.command == PCommands.sendResults:
      results_bool = json.loads(message.args)
      if results_bool:
          client_socket.setblocking(True)
          results_PObject = p.receivePObject(client_socket)
          client_socket.setblocking(False)
          results = results_PObject.object
          exception = False
          return results, exception
      else:
          results = False
          exception = False
          return results, exception
  elif message.command == PCommands.exception:
      results = False
      exception = message.args
      return results, exception

def requestInsertQuery(client_socket: socket.socket, user: OMSUser, query_string: str):
  p = Protocol()
  p.sendQuery(client_socket,PCommands.select_query, user, query_string)
  client_socket.setblocking(True)
  message = p.receiveMessage(client_socket)
  client_socket.setblocking(False)
  if message.command == PCommands.sendResults:
      result_bool = json.loads(message.args)
      result = result_bool
      exception = False
      return result, exception
  elif message.command == PCommands.exception:
      result = False
      exception = message.args
      return result, exception