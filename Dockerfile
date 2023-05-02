FROM python:3.11.2-bullseye

WORKDIR /app

COPY . /app/

RUN pip install -r requirements.txt

CMD [ "python", "main.py" ]