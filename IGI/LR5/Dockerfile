FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV PORT=8000
ENV DJANGO_SUPERUSER_USERNAME=admin
ENV DJANGO_SUPERUSER_PASSWORD=admin123

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN adduser --disabled-password --gecos "" appuser && \
    mkdir -p /app/logs /app/media /app/staticfiles && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD sh -c "python manage.py migrate && \
           python manage.py collectstatic --noinput && \
           python manage.py create_admin && \
           gunicorn confectionery_shop.wsgi:application --bind 0.0.0.0:${PORT}"