FROM python:3.7

EXPOSE 5000

WORKDIR /flask

ENV FLASK_APP api

COPY . /flask

RUN pip install --upgrade pip setuptools

RUN pip install six wheel

RUN pip install mysql-client

RUN pip install -r requirements.txt

CMD ["flask", "run"]