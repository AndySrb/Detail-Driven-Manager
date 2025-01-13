FROM python:3.13.1-bullseye

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r  requirements.txt

COPY app.py /app/

CMD ["flask","run","--host","0.0.0.0"] 



