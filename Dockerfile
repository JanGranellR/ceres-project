FROM ariqbasyar/opencv:v4.8.1.78-py3.9.18

RUN mkdir /app
RUN mkdir /app/data
RUN mkdir /app/data/models
WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY config /app/config
COPY test /app/test
COPY app.py /app

EXPOSE 7860

CMD [ "python3", "/app/app.py" ]