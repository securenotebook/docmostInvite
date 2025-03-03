FROM python:3.11-slim

# Set working directory in the container
WORKDIR /app

# Install dependencies
RUN pip install psycopg2-binary

# Copy scripts and CSV into the container
COPY invite_script.py .
COPY create_invites.py .
COPY invites.csv .

# Copy the Bash scripts
COPY run_create_invites.sh .
COPY run_list_invites.sh .

# Make them executable
RUN chmod +x /app/run_create_invites.sh /app/run_list_invites.sh

# Default to listing invites (optional)
CMD ["/app/run_list_invites.sh"]
