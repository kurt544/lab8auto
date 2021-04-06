
FROM python:3.8-slim

ADD . /program

WORKDIR /program

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY src/ .

EXPOSE 5000

CMD ["python3", "./api.py"]
