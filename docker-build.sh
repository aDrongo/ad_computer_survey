docker network create lds

docker build router/ -t lds-router
docker run -p 80:80 -p 443:443 -d --restart always --network lds --name lds-router lds-router

docker build backend/ -t lds-backend
docker run -p 5000:5000 -d --restart always --network lds --name lds-backend lds-backend

docker build frontend/ -t lds-frontend
docker run -p 8080:8080 -d --restart always --network lds --name lds-frontend lds-frontend