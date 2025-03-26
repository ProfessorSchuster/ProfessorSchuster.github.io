# Dockerfile (lokal)
FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        chromium \
        chromium-driver \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

ENV CHROME_BINARY=/usr/bin/chromium

CMD ["python", "update_price.py"]