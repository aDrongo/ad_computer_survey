# LDAP Device Surveyor
The purpose of this program is to easily scan AD computers and see their status by their location.
* Python for API, scanning module, ldap and SQL interaction.
* Vue.JS SPA frontend, makes ajax calls to API for data.
* Displays devices by subnet locations with an overview and collapsed tables.
* Scans LDAP and pulls devices from specified OUs.
* Intiate a Scan of all devices or just a single device by clicking on it.
* Set interval for periodic scanning, default 5 minutes.
* Add or Remove Devices manually as well.
* Add, Remove or Reset Users.
* Must be logged in to modify devices/users or view logs.
* Docker build optional

Work in progress

ToDo:
* HTTPS
* Secure config.  
* Log history of device state changes.  
* Specific Device History?
* User Authorization for roles to edit devices and/or users?

## Example Images

https://ibb.co/H4Byyrq  
https://ibb.co/rcGnZj8  
https://ibb.co/WDQ3MRc  

## Install via Docker

```
git clone https://github.com/aDrongo/ldap-device-surveyor.git

cd ldap-device-surveyor/backend
docker build . -t lds-backend
docker run -p 5000:5000 -d lds-backend

#To store databse edit config database location to an attached docker volume.

cd ../frontend
docker build . -t lds-frontend
docker run -p 80:80 -d lds-frontend
```