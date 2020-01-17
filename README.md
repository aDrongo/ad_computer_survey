# LDAP Device Surveyor
The purpose of this program is to ping an OU of computers.
* Discovery is where it pulls from LDAP and pings devices pulled
* Uses async module for pinging, enables concurrency for faster processing.
* By default it runs discovery every 10 minutes
* Uses a SQLLite database to store data
* Records last successful pinged time
* It cross-checks it's database with LDAP every 12hrs
* It can show LastLogon timestamp to identify inactive computers
* You can filter the devices pulled from LDAP
* It can display attributes pulled from LDAP
* It can organize by location
* LDAP API to modify objects

Work in progress.  

## Install
git clone this repo  
sudo apt-get install python3.7 python3-pip   
python3.7 -m pip install -r requirements.txt  
useradd --user-group flask  
sudo chown flask:flask .* -R  
sudo chmod 775 .* -R  

## Install SSL Certs as server.x509 & server.key
You can change web.py to not use SSL  

## Initialize database
python3.7 discovery.py  

## Create Service
sudo vim /etc/systemd/system/lds.service  

```[Unit]  
Description=LDAP Device Surveyor  
Requires=network.target  
After=network.target  
After=syslog.target  

[Service]  
User=flask 
Group=flask  
ExecStart=/usr/bin/python3.7 /opt/ldap_device_surveyor/package/web.py  
WorkingDirectory=/opt/ldap_device_surveyor/package
Restart=always  

[Install]  
WantedBy=multi-user.target
```

sudo systemctl daemon-reload --force  
sudo systemctl enable lds.service  
sudo systemctl start lds.service  


## API
Example  
```
/api/v1/modify/computer=NWMSVMMJ1699&description=ben.gardner.test&extensionAttribute2=Puyallup%20400&extensionAttribute3=1334566439&extensionAttribute5=0
```

Fields are  
```
computer *required  
description  
extensionAttribute2  
extensionAttribute3  
extensionAttribute5  
```

It will fail if wrong fields are submited or no computer included, returns JSON with results.  