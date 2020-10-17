FROM ubuntu:latest

RUN apt-get update -q -y
RUN apt-get install python3-pip -q -y
RUN pip3 install flask

WORKDIR /home/edts-flask
COPY back-end /home/edts-flask

RUN pip3 install -r requirements.txt

EXPOSE 5000

#CMD [“python3”,”hello.py”]
