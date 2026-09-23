FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app

COPY CyberAttackPrediction/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir gunicorn

COPY CyberAttackPrediction /app/CyberAttackPrediction

EXPOSE 8080

CMD ["sh", "-c", "cd /app/CyberAttackPrediction && gunicorn --bind 0.0.0.0:${PORT:-8080} Main:app"]
