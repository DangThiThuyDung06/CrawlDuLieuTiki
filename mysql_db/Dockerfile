FROM mysql:8.0.32
ENV MYSQL_ROOT_PASSWORD 123456
ADD ./init_db /docker-entrypoint-initdb.d
EXPOSE 3306