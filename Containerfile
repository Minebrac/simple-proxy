FROM python:3.11

WORKDIR /proxy
COPY ./proxy .

EXPOSE 30625

ENTRYPOINT ["python", "-u", "main.py"]