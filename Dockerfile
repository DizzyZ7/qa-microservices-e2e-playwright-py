FROM mcr.microsoft.com/playwright/python:v1.46.0-jammy

WORKDIR /work

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN playwright install --with-deps

CMD ["pytest"]
