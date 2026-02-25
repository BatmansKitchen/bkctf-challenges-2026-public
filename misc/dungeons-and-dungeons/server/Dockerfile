FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY .env .

EXPOSE 5000

ENV MAX_CONNECTIONS=100
ENV PORT=5000

CMD ["/bin/bash", "-c", "export $(cat .env | xargs) && python /app/main.py"]