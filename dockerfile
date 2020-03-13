FROM python:3
ADD uc_oms_server.py /uc-oms-server
ADD uc_oms_protocol.py /uc-oms-server
EXPOSE 4444
WORKDIR /uc-oms-server
CMD [ "python", "./uc-oms-server" ]