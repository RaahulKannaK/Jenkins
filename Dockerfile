FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir 'Flask>=3.0,<4.0' 'gunicorn>=22.0,<24.0'
COPY app.py .
EXPOSE 5000
USER nobody
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
