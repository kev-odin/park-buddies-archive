### START CLASS IMAGE ###
FROM PYTHON:3.10-slim-buster as class
RUN pip install email_validator flask flask-wtf flask-login flask-sqlalchemy requests

### https://blog.tanka.la/2021/08/28/debugging-python-application-in-docker-using-vscode/ ###
### START BASE IMAGE ###
FROM PYTHON:3.10-slim-buster as base
RUN mkdir /app
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY ./ /app/

### START DEBUG IMAGE ###
FROM base as debug
RUN pip install black debugpy
CMD python -m debugpy --listen 0.0.0.0:5678 --wait-for-client -m flask run -h 0.0.0.0 -p 5000

### START PRODUCTION IMAGE ###
FROM base as prod
CMD flask run -h 0.0.0.0 -p 5000