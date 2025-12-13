FROM python:3.13

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential gcc git postgresql-client --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

RUN chmod +x /app/scripts/wait-for-db.sh

ENV PYTHONUNBUFFERED=1
ENV PYTHONFAULTHANDLER=1
ENV PYTHONPATH="/app"
ENV PYTHONDONTWRITEBYTECODE=1