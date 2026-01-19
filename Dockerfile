FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip && pip install -r /tmp/requirements.txt && rm -rf /root/.cache/

COPY . /code

EXPOSE 8000

CMD sh -c "python manage.py collectstatic --noinput && gunicorn --bind :8000 --workers 2 config.wsgi"
