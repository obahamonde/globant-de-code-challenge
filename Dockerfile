FROM python:3.9.7-slim-buster

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt && \
    prisma db push && \
    prisma generate

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000","--reload"]
