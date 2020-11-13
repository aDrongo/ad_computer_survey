# Frontend LDS

## Install
sudo apt-get npm  
npm install -g serve  

npm install  
npm run build  

## Create Service for permenant Run
sudo vim /etc/systemd/system/lds-serve.service  

```[Unit]  
Description=LDAP Device Surveyor Website
Requires=network.target  
After=network.target  
After=syslog.target  

[Service]  
User=lds 
Group=lds  
ExecStart=/usr/bin/serve -l 80
WorkingDirectory=/opt/ldap-device-surveyor/frontend/dist
Restart=always  

[Install]  
WantedBy=multi-user.target
sudo systemctl daemon-reload --force  
sudo systemctl enable lds-serve.service  
sudo systemctl start lds-serve.service 
```
