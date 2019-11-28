FROM python:3.7

RUN apt-get update
RUN apt-get install -y libzbar0 libzbar-dev

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

CMD [ "python", "./app.py" ]



