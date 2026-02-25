FROM python:3.11-slim

WORKDIR /app

RUN pip install flask --no-cache-dir

COPY tokens.py safehtml.py app.py ./
COPY static/ ./static/
COPY templates/ ./templates/

ENV FLAG=bkctf{fu11y_r3m0v3d_x55_but_4t_wh4t_c0st}
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["python", "app.py"]