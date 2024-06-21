FROM python:3.12

WORKDIR /data

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 80
ENTRYPOINT ["python3", "server.py"]
#CMD python3 server.py
