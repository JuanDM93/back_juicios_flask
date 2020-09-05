FROM python:3.8.5

EXPOSE 5000

WORKDIR /flask
COPY . .

RUN pip install --upgrade pip setuptools
RUN pip install wheel six

RUN pip install -r requirements.txt

ENV FLASK_APP api

CMD ["flask", "run", "-h", "0.0.0.0", "--no-reload"]