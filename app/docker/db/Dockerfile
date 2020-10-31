FROM postgres:latest
ENV POSTGRES_PASSWORD newhat
ENV POSTGRES_USER edts
ENV POSTGRES_DB edts

WORKDIR /home/edts
COPY default.sql /docker-entrypoint-initdb.d
