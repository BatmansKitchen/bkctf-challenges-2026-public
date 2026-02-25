# Use a lightweight Python base image
FROM python:3.15-rc-alpine

# Set working directory inside the container
WORKDIR /app

# Set environment variables (Best Practice: keeps Python from buffering stdout)
ENV PYTHONUNBUFFERED=1

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the code
COPY . .

EXPOSE 5000

# Default command to run the app
CMD ["python", "app.py"]