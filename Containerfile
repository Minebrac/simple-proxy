FROM python:3.10.20-alpine3.22

WORKDIR /proxy
COPY ./proxy .

EXPOSE 30625

ENTRYPOINT ["python", "main.py"]