FROM postgres:latest
ENV POSTGRES_PASSWORD newhat
ENV POSTGRES_USER edts
ENV POSTGRES_DB triagedb

WORKDIR /home/edts
COPY TriageDB.sql /docker-entrypoint-initdb.d
