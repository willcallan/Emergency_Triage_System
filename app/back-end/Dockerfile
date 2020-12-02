FROM ubuntu:20.10

RUN apt-get update -q -y
RUN apt-get install python3-pip -q -y
RUN apt install libpq-dev -y
RUN pip3 install flask

WORKDIR /home/edts-flask
COPY . /home/edts-flask

RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD python3 app.py
