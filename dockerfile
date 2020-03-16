FROM python:3
ADD uc_oms_server.py /
ADD uc_oms_protocol.py /
ADD db_interface.py /
ADD requirements.txt /
RUN pip install -r requirements.txt
EXPOSE 4444
CMD [ "python", "./uc_oms_server.py" ]