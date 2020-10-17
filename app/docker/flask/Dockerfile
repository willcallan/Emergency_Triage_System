FROM ubuntu:latest

RUN apt-get update -q -y
RUN apt-get install python3-pip -q -y
RUN apt-get install python3-flask -q -y
RUN apt-get install python3-flask-api -q -y

ADD back-end /edts-flask
WORKDIR /edts-flask
EXPOSE 5000

#CMD [“python3”,”hello.py”]
