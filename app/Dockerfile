FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

ENV REDIS_HOST=redis-service
ENV REDIS_PORT=6379

CMD ["python", "app.py"]
