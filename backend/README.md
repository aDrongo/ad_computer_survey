# Backend LDS

## Install python & lds 
cd /opt  
git clone this repo  
sudo apt-get install python3 python3-pip   #at least python3.7  
python3 -m pip install -r requirements.txt  
useradd --user-group lds  
sudo chown lds:lds ldap-device-surveyor/ -R  
sudo chmod 4775 ldap-device-surveyor/ -R  

## Setup config file
vim ldap-device-surveyor/backend/config.json

## Setup SSL
Create SSL Certs as server.x509 & server.key and enable environmental variable 'PROD'

## Initialize application and test.
python3 modules/init.py  
python3 main.py  

localhost:5000/api/scan  
localhost:5000/api/devices  

## Create Service for permenant Run
sudo vim /etc/systemd/system/lds.service  

```[Unit]  
Description=LDAP Device Surveyor  
Requires=network.target  
After=network.target  
After=syslog.target  

[Service]  
User=lds 
Group=lds  
ExecStart=/usr/bin/python3.7 /opt/ldap-device-surveyor/backend/main.py  
WorkingDirectory=/opt/ldap-device-surveyor/backend
Restart=always  

[Install]  
WantedBy=multi-user.target
sudo systemctl daemon-reload --force  
sudo systemctl enable lds.service  
sudo systemctl start lds.service 
```