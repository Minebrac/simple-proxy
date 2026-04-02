FROM python:3.11.15-slim-trixie

WORKDIR /proxy
COPY ./proxy .
COPY requirements.txt .

RUN ["pip", "install", "-r", "requirements.txt"]

EXPOSE 30625

ENTRYPOINT ["python", "-u", "main.py"]