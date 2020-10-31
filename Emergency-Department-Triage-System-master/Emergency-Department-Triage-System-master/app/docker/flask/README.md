#Quick start
% bash buildNKickoff.sh


# Create Docker Container
% cp ../../back-end .
% docker build -t edts-flask:1.1 .<br>
% docker create --name edts-flask -P -t -p 5000:5000 edts-flask:1.1<br>
% docker start edts-flask<br>


# Notes
It does not auto start the app currently.  Don't know what is going on there as of yet. But it can be started manually with:<br>
% docker exec -it edts-flask python3 hello.py<br>

I also don't currently know why that I can't access the app from outside the container but I can inside.  I can tell that the port is active and trying to do something, but I am prevented from pulling the app.
