FROM python:3.11-slim

RUN apt-get update -y && apt-get upgrade -y && apt-get install chromium -y

WORKDIR /parser

COPY . .

RUN pip install -r requirements.txt --no-cache-dir

CMD ["python", "main.py"]