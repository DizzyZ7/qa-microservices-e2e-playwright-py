FROM python:3.12-slim

WORKDIR /app

COPY app/ /app/app/
RUN pip install --no-cache-dir fastapi uvicorn sqlalchemy psycopg2-binary pydantic pydantic-settings

ENV PYTHONPATH=/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
