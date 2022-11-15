FROM python:3.9.2
USER root

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

RUN apt-get update
RUN apt-get install -y ffmpeg

CMD ["python","bot.py"]
