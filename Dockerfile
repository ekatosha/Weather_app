FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /weather
WORKDIR /weather
ADD requirements.txt /weather/
RUN pip install -r requirements.txt
ADD . /weather/