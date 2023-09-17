FROM python:3.11.1
LABEL authors="Alex"


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /educa

COPY requirements.txt /educa/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY educa /educa/