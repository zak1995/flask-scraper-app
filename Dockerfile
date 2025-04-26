FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN apt-get update && apt-get install -y \
    wget curl unzip fonts-liberation libnss3 libatk1.0-0 libatk-bridge2.0-0 \
    libxcomposite1 libxrandr2 libgbm1 libgtk-3-0 libasound2 libxdamage1 libxshmfence1 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt
RUN python -m playwright install --with-deps

EXPOSE 10000

CMD ["python", "main.py"]

