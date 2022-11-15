FROM python:3.9.2
USER root

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip

RUN pip install -r /app/requirements.txt

CMD ["python","bot.py"]
