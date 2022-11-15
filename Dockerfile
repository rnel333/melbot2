FROM python:3.9.2
USER root

RUN pip install --upgrade -r requirements.txt
