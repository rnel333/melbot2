FROM python:3.9.2
USER root

COPY . .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt
