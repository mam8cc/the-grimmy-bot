FROM python:3.10.13-slim-bullseye
WORKDIR /opt/app
COPY . .
RUN pip install -r requirements.txt

CMD python bot.py