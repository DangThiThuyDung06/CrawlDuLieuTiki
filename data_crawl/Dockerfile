FROM python:3.9.13-slim-buster
COPY . /data_crawl
RUN apt-get update && apt-get install -y curl&&\
    pip install fastapi uvicorn requests pandas
WORKDIR /data_crawl
CMD ["uvicorn", "main_crawl:app", "--host", "0.0.0.0", "--port", "8000"]

