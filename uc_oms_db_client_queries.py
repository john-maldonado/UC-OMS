import time
import socket

from uc_oms_protocol import OMSUser
from uc_oms_db_funcs import assembleSQLFields, requestSelectQuery, requestInsertQuery, requestUpdateQuery, requestDeleteQuery

def query_selectBasic(client_socket, user):
  table = "sales_orders"
  fields = ['so_id', 'entered_ts', 'so_number', 'description', 'customer', 'order_date', 'closed']
  fieldsString = assembleSQLFields(fields)
  sql = "SELECT {} FROM {}"
  sql = sql.format(fieldsString, table)
  results, exception = requestSelectQuery(client_socket, user, sql)
  return results, fields, exception

def query_selectAll(client_socket: socket.socket, user: OMSUser):
  table = "sales_orders"
  fields = ['so_id', 'entered_ts', 'so_number', 'description', 'customer', 'order_date', 'due_date', 'quote_number', 'customer_po', 'completed_date', 'completed', 'invoiced', 'invoice_number', 'invoice_date', 'invoice_amount', 'paid_full', 'paid_date', 'paid_amount', 'closed']
  fieldsString = assembleSQLFields(fields)
  sql = "SELECT {} FROM {}"
  sql = sql.format(fieldsString, table)
  results, exception = requestSelectQuery(client_socket, user, sql)
  return results, fields, exception

def query_selectAllOpen(client_socket, user):
  table = "sales_orders"
  fields = ['so_id', 'so_number', 'description', 'customer', 'order_date','due_date', 'completed', 'invoiced', 'invoice_amount', 'paid_amount', 'paid_full']
  fieldsString = assembleSQLFields(fields)
  condition = "closed = 0"
  sql = "SELECT {} FROM {} WHERE {}"
  sql = sql.format(fieldsString, table, condition)
  results, exception = requestSelectQuery(client_socket, user, sql)
  return results, fields, exception

def query_insertIntoTimeLog(client_socket: socket.socket, user: OMSUser, SalesOrder):
  SalesOrderString = "{}".format(SalesOrder)
  TimeStamp = "{}".format(time.strftime('%Y-%m-%d %H:%M:%S'))
  table = "time_log"
  fields = ['so_number', 'clockin_ts']
  fieldsString = assembleSQLFields(fields)
  values = "'{}', '{}'"
  values = values.format(SalesOrderString,TimeStamp)
  sql = "INSERT INTO {} ({}) VALUES ({})"
  sql = sql.format(table, fieldsString, values)
  result, exception = requestInsertQuery(client_socket, user, sql)
  return result, fields, exception

def query_selectTimeLogBySO(client_socket: socket.socket, user: OMSUser, SalesOrder):
  SalesOrderString = "{}".format(SalesOrder)
  table = "time_log"
  fields = ['log_id', 'so_number', 'clockin_ts', 'clockout_ts', 'activity']
  fieldsString = assembleSQLFields(fields)
  condition = "so_number='{}'"
  condition = condition.format(SalesOrderString)
  sql = "SELECT {} FROM {} WHERE {}"
  sql = sql.format(fieldsString, table, condition)
  results, exception = requestSelectQuery(client_socket, user, sql)
  return results, fields, exception

def query_updateTimeLogClockOut(client_socket: socket.socket, user: OMSUser, logID, activity):
  TimeStamp = "{}".format(time.strftime('%Y-%m-%d %H:%M:%S'))
  ActivityString = "{}".format(activity)
  fields = ['clockout_ts', 'activity']
  sql = "UPDATE time_log SET clockout_ts='{}', activity='{}' WHERE log_id={}"
  sql = sql.format(TimeStamp,ActivityString,logID)
  result, exception = requestUpdateQuery(client_socket, user, sql)
  return result, fields, exception

def query_selectClockinClockoutBySO(client_socket: socket.socket, user: OMSUser, SalesOrder):
  SalesOrderString = "{}".format(SalesOrder)
  table = "time_log"
  fields = ['log_id', 'so_number', 'clockin_ts', 'clockout_ts', 'activity']
  fieldsString = assembleSQLFields(fields)
  condition = "so_number='{}'"
  condition = condition.format(SalesOrderString)
  sql = "SELECT {} FROM {} WHERE {}"
  sql = sql.format(fieldsString, table, condition)
  results, exception = requestSelectQuery(client_socket, user, sql)
  return results, fields, exception

def query_selectTimeLogByLogID(client_socket: socket.socket, user: OMSUser, logID):
  table = "time_log"
  fields = ['log_id', 'so_number', 'clockin_ts', 'clockout_ts', 'activity']
  fieldsString = assembleSQLFields(fields)
  condition = "log_id='{}'"
  condition = condition.format(logID)
  sql = "SELECT {} FROM {} WHERE {}"
  sql = sql.format(fieldsString, table, condition)
  results, exception = requestSelectQuery(client_socket, user, sql)
  return results, fields, exception

def query_deleteTimeLogByLogID(client_socket: socket.socket, user: OMSUser, logID):
  table = "time_log"
  condition = "log_id='{}'"
  condition = condition.format(logID)
  sql = "DELETE FROM {} WHERE {}"
  sql = sql.format(table, condition)
  result, exception = requestDeleteQuery(client_socket, user, sql)
  return result, exception

def query_selectSalesOrderBySONumber(client_socket: socket.socket, user: OMSUser, SalesOrder):
  SalesOrderString = "{}".format(SalesOrder)
  table = "sales_orders"
  fields = ['so_id', 'entered_ts', 'so_number', 'description', 'customer', 'order_date', 'due_date', 'quote_number', 'customer_po', 'completed_date', 'completed', 'invoiced', 'invoice_number', 'invoice_date', 'invoice_amount', 'paid_full', 'paid_date', 'paid_amount', 'closed']
  fieldsString = assembleSQLFields(fields)
  condition = "so_number='{}'"
  condition = condition.format(SalesOrderString)
  sql = "SELECT {} FROM {} WHERE {}"
  sql = sql.format(fieldsString, table, condition)
  results, exception = requestSelectQuery(client_socket, user, sql)
  return results, fields, exception

def query_selectSalesOrderBySONumberShort(client_socket: socket.socket, user: OMSUser, SalesOrder):
  SalesOrderString = "{}".format(SalesOrder)
  table = "sales_orders"
  fields = ['so_number', 'description', 'customer', 'order_date', 'due_date', 'quote_number', 'customer_po', 'completed_date', 'completed', 'invoiced', 'invoice_number', 'invoice_date', 'invoice_amount', 'paid_full', 'paid_date', 'paid_amount', 'closed']
  fieldsString = assembleSQLFields(fields)
  condition = "so_number='{}'"
  condition = condition.format(SalesOrderString)
  sql = "SELECT {} FROM {} WHERE {}"
  sql = sql.format(fieldsString, table, condition)
  results, exception = requestSelectQuery(client_socket, user, sql)
  return results, fields, exception

def query_selectSalesOrderByCustomer(client_socket: socket.socket, user: OMSUser, Customer):
  CustomerString = "{}".format(Customer)
  table = "sales_orders"
  fields = ['so_id', 'entered_ts', 'so_number', 'description', 'customer', 'order_date', 'due_date', 'quote_number', 'customer_po', 'completed_date', 'completed', 'invoiced', 'invoice_number', 'invoice_date', 'invoice_amount', 'paid_full', 'paid_date', 'paid_amount', 'closed']
  fieldsString = assembleSQLFields(fields)
  condition = "customer='{}'"
  condition = condition.format(CustomerString)
  sql = "SELECT {} FROM {} WHERE {}"
  sql = sql.format(fieldsString, table, condition)
  results, exception = requestSelectQuery(client_socket, user, sql)
  return results, fields, exception
  
def query_selectMaxSalesOrder(client_socket: socket.socket, user: OMSUser):
  table = "sales_orders"
  field = "so_number"
  sql = "SELECT MAX({}) FROM {}"
  sql = sql.format(field, table)
  results, exception = requestSelectQuery(client_socket, user, sql)
  return results, field, exception

def query_insertIntoSalesOrders(client_socket: socket.socket, user: OMSUser, salesOrder, description, customer, orderDate, dueDate):
  table = "sales_orders"
  fields = ['so_number', 'description', 'customer', 'order_date', 'due_date']
  fieldsString = assembleSQLFields(fields)
  values = "'{}', '{}', '{}', '{}', '{}'"
  values = values.format(salesOrder, description, customer, orderDate, dueDate)
  sql = "INSERT INTO {} ({}) VALUES ({})"
  sql = sql.format(table,fieldsString,values)
  result, exception = requestInsertQuery(client_socket, user, sql)
  return result, exception

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