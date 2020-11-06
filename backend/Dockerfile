FROM ubuntu:latest
LABEL maintainer="ben gardner <ben.gardner@nwmotorsport.com>"

RUN mkdir /opt/ldap-device-surveyor/backend/ -p
COPY . /opt/ldap-device-surveyor/backend/

RUN apt-get update && \
apt-get install -y --no-install-recommends \
python3.8 python3-pip iputils-ping && \
pip3 install -r /opt/ldap-device-surveyor/backend/requirements.txt && \
python3.8 /opt/ldap-device-surveyor/backend/modules/init.py

EXPOSE 5000

#ENV PROD=PROD

WORKDIR /opt/ldap-device-surveyor/backend/
ENTRYPOINT ["/bin/python3.8","/opt/ldap-device-surveyor/backend/main.py"]