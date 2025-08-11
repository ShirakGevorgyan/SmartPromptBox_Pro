FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements*.txt ./
RUN python -m pip install --upgrade pip && \
    if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

COPY app/ ./app/

RUN mkdir -p db

HEALTHCHECK --interval=30s --timeout=5s --retries=5 \
CMD python -c "import app; print('ok')" || exit 1

CMD ["python3", "-m", "app.telegram_bot.bot"]
