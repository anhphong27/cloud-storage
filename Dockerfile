FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install  -r requirements.txt

COPY . .

WORKDIR /app/app

ENV FLASK_APP=index.py

ENV FLASK_ENV=production

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "index:app"]