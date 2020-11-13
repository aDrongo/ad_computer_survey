docker rm -f lds-backend
docker build backend/ -t lds-backend
docker run -p 5000:5000 -d --restart always --name lds-backend lds-backend

docker rm -f lds-frontend
docker build /fronted -t lds-frontend
docker run -p 80:80 -d --restart always -d lds-frontend