FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

#CMD ["python", "server.py"]
ENTRYPOINT ["python3", "server.py"]