sudo apt-get install python3.7 python3-pip  
python3.7 -m pip install -r requirements.txt  
useradd --user-group flask  
sudo chown flask:flask .* -R  
sudo chmod 755 .* -R  

Install SSL Certs

sudo vim /etc/systemd/system/lds.service

[Unit]  
Description=LDAP Device Surveyor  
Requires=network.target  
After=network.target  
After=syslog.target  

[Service]  
User=administrator  
Group=administrator  
ExecStart=/usr/bin/python3.7 /opt/ldap_device_surveyor/main/web.py  
WorkingDirectory=/opt/ldap_device_surveyor/main
Restart=always  

[Install]  
WantedBy=multi-user.target  
~

sudo systemctl daemon-reload --force  
sudo systemctl enable lds.service  
sudo systemctl start lds.service  
