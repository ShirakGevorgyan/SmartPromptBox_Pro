# devops/docker/app/Dockerfile

FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY tests/ ./tests/
COPY devops/ ./devops/
COPY db/ ./db/
COPY init_db_once.py ./
COPY README.md ./

CMD ["python3", "-m", "app.telegram_bot.bot"]