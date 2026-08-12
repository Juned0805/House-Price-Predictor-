FROM python:3.10-slim

WORKDIR /app

# Copy dependencies list first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose port and run the app
EXPOSE 5000
CMD ["python", "app.py"]
