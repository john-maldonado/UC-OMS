# UC OMS Setup
Installation and setup instructions for Ulitmate Controls Order Managment System

## Server Setup
```bash
git clone git@github.com:greenbean209/UC-OMS.git
cd ./UC-OMS
sudo docker build -t uc-oms-server .
sudo ufw allow in on docker0 to any app MariaDB
sudo docker run -d -p 4444:4444 --restart unless-stopped uc-oms-server
```

## Client Setup
```bash
git clone git@github.com:greenbean209/UC-OMS.git
do something else
```