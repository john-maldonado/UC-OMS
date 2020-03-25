import socket
import json

from uc_oms_protocol import Protocol, PCommands, OMSUser

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
  p.sendQuery(client_socket,PCommands.insert_query, user, query_string)
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

def requestUpdateQuery(client_socket: socket.socket, user: OMSUser, query_string: str):
  p = Protocol()
  p.sendQuery(client_socket,PCommands.update_query, user, query_string)
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

def requestDeleteQuery(client_socket: socket.socket, user: OMSUser, query_string: str):
  p = Protocol()
  p.sendQuery(client_socket,PCommands.delete_query, user, query_string)
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