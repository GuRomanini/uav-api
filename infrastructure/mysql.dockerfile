FROM mysql:latest

ENV PORT=5432
ENV MYSQL_DATABASE service_handler
ENV MYSQL_ROOT_PASSWORD default
ENV MYSQL_USER romanini
ENV MYSQL_PASSWORD default

COPY ./infrastructure/database.sql /docker-entrypoint-initdb.d/
# COPY ./infrastructure/grants.sql /docker-entrypoint-initdb.d/

EXPOSE 3306