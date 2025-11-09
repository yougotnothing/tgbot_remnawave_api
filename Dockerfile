FROM python:3.11.8-alpine

WORKDIR /usr/src/api/

COPY requirements.txt /usr/src/api/
RUN pip install -r /usr/src/api/requirements.txt
COPY . /usr/src/api/

CMD 'fastapi run main.py --port 7575'
