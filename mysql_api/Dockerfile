FROM python:3.9.13-slim-buster
COPY . /mysql_api
RUN pip install fastapi uvicorn mysql-connector-python requests numpy pandas
WORKDIR /mysql_api
CMD ["uvicorn", "main_mysqlapi:app", "--host", "0.0.0.0", "--port", "7100"]