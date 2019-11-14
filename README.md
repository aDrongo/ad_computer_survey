# LDAP Device Surveyor
The purpose of this program is to ping an OU of computers.
..* It can show LastLogon timestamp to identify inactive computers
..* You can filter the devices pulled from LDAP
..* It can organize by location
..* It can display attributes pulled from LDAP
..* Discovery is where it pulls from LDAP and pings device pulled
..* By default it runs discovery every 10 minutes
..* Uses a SQLLite database to store data
..* Records last pinged time
..* It cross-checks it's database with LDAP every 12hrs

Work in progress.
TODO: Rewrite program to a more modular format with classes that doesn't rely upon calling individual python scripts.
TODO: Add modularity to allow easy adding/removing of attributes


## Install Python3.7
git clone git@github.com:NorthwestMotorsport/ldap_device_surveyor.git
sudo apt-get install python3.7 python3-pip
cd ldap_device_surveyor
python3.7 -m pip install -r requirements.txt
useradd --user-group flask  
sudo chown flask:flask .* -R 
sudo chmod 775 .* -R  

## Install SSL Certs as server.x509 & server.key

## Initialize database
python3.7 discovery.py

## Create Service
sudo vim /etc/systemd/system/lds.service

`[Unit]  
Description=LDAP Device Surveyor  
Requires=network.target  
After=network.target  
After=syslog.target  

[Service]  
User=flask 
Group=flask  
ExecStart=/usr/bin/python3.7 /opt/ldap_device_surveyor/main/web.py  
WorkingDirectory=/opt/ldap_device_surveyor/main
Restart=always  

[Install]  
WantedBy=multi-user.target`

sudo systemctl daemon-reload --force  
sudo systemctl enable lds.service  
sudo systemctl start lds.service  
