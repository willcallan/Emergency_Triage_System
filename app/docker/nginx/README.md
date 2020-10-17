# Build App
From the front-end directory

% ng build --prod<br>
% cp -r dist ../docker

# Create Docker Container
% cd ../docker<br>
% docker build -t edts:1.1 .<br>
% docker create --name edts-docker -P -t -p 80:80 edts:1.1<br>
% docker start edts-docker<br>
