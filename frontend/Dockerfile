# If you want to build yourself
#FROM node:latest as build-stage
#WORKDIR /app
#COPY package.json ./
#RUN npm install
#COPY ./ .
#RUN npm run build

FROM nginx as production-stage
LABEL maintainer="ben gardner <mail@ben-gardner.com>"
RUN mkdir /app
COPY dist/ /app
#COPY server.key /etc/nginx/certs/
#COPY server.crt /etc/nginx/certs/
COPY nginx.conf /etc/nginx/nginx.conf