FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements*.txt ./
RUN python -m pip install --upgrade pip && \
    if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

COPY app/ ./app/
COPY tests/ ./tests/
COPY devops/ ./devops/

RUN mkdir -p db

CMD ["python3", "-m", "app.telegram_bot.bot"]
