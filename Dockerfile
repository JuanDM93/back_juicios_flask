FROM python:3.7

ENV TZ=America/Mexico_City
RUN apt-get update -y
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /flask
COPY . .

RUN pip install --upgrade pip setuptools
RUN pip install wheel six

RUN pip install -r requirements.txt

ENV FLASK_APP api

EXPOSE 5000

CMD ["flask", "run", "-h", "0.0.0.0", "--no-reload"]
