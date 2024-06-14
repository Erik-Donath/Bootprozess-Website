LABEL authors="erikd"

FROM python:3.8-slim-buster

WORKDIR /data

COPY requirements.txt requirements.txt
RUN pip3 -m venv venv
RUN source /venv/bin/activate
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=80"]

ENTRYPOINT ["top", "-b"]