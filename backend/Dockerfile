FROM ubuntu:latest
LABEL maintainer="ben gardner <mail@ben-gardner.com>"

RUN mkdir /opt/ldap-device-surveyor/backend/ -p
COPY . /opt/ldap-device-surveyor/backend/

RUN apt-get update && \
apt-get install -y --no-install-recommends \
python3.8 python3-pip iputils-ping && \
pip3 install -r /opt/ldap-device-surveyor/backend/requirements.txt

WORKDIR /opt/ldap-device-surveyor/backend/
RUN python3.8 /opt/ldap-device-surveyor/backend/init.py

EXPOSE 5000
ENTRYPOINT ["gunicorn","--bind", "0.0.0.0:5000", "wsgi:app"]
#Insert following to entrypoint array for SSL
# ,"--certfile=server.crt", "--keyfile=server.key"

#Development optional server
#ENTRYPOINT ["/bin/python3.8","/opt/ldap-device-surveyor/backend/main.py"]