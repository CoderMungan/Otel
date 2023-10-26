FROM python:3.12

ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


WORKDIR /home/OtelApp

COPY requirements.txt /home/OtelApp/

RUN pip install -r requirements.txt

COPY . .