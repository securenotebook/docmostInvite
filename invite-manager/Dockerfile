FROM python:3.11-slim

# Set working directory in the container
WORKDIR /app

# Install dependencies
RUN pip install psycopg2-binary

# Copy the Python script into the container
COPY invite_script.py .

# Run the script on startup
CMD ["python", "invite_script.py"]
