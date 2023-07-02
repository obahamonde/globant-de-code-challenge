FROM python:3.9.7-slim-buster

WORKDIR /app

COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt && \
    python -m prisma db push --force-reset && \
    python -m prisma generate && \
    python -m prisma py fetch

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
