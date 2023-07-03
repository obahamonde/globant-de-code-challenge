FROM python:3.9.7-slim-buster

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt && \
    prisma generate

EXPOSE 5000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]
