FROM python:3
ADD uc_oms_server.py /
ADD uc_oms_protocol.py /
EXPOSE 4444
CMD [ "python", "./uc_oms_server.py" ]