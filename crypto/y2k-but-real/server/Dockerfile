FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy the server script
COPY server.py /app/
RUN chmod +x /app/server.py

EXPOSE 1999

# ctf user
RUN useradd -m -u 1000 ctf && chown -R ctf:ctf /app
USER ctf

CMD ["python3", "/app/server.py"]