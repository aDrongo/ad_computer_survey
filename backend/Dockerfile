FROM python:3
LABEL maintainer="ben gardner <mail@ben-gardner.com>"

RUN mkdir /opt/ldap-device-surveyor/backend/ -p

WORKDIR /opt/ldap-device-surveyor/backend/

COPY . .

RUN pip3 install -r /opt/ldap-device-surveyor/backend/requirements.txt

EXPOSE 5000
ENTRYPOINT ["gunicorn","--bind", "0.0.0.0:5000", "wsgi:application"]

#Development optional server
#ENTRYPOINT ["python","/opt/ldap-device-surveyor/backend/app.py"]