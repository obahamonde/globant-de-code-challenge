FROM python:3.9.7-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r --no-cache-dir requirements.txt

RUN prisma db push && \
    prisma generate && \
    prisma py fetch

COPY . .

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
