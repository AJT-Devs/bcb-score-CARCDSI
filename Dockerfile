FROM python:3.14.0-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/app/src

WORKDIR /app

COPY requirements.txt ./

RUN python -m pip install --upgrade "pip==26.3" \
    && python -m pip install -r requirements.txt

COPY src/ ./src/

CMD ["python", "--version"]
