FROM python:3.13.1-alpine3.21

WORKDIR /app

COPY . /app

RUN pip install -r  requirements.txt

EXPOSE 5000


CMD cd app && flask run --host 0.0.0.0
