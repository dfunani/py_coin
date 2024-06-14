# Use an appropriate base image for your Flask application
FROM python:3.12

# Set the working directory within the container
WORKDIR /app

# Install required packages
RUN apt-get update \
    && apt-get install -y \
    openssh-client \
    git \
    postgresql-client \
    netcat-openbsd \
    && apt-get clean

# Copy the necessary files
COPY . .

# Copy the wait-for-it script
RUN chmod +x /app/db/test_db_migration.sh

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
COPY test.env .env
# Load environment variables from .env file
RUN export $(cat .env | xargs)

# Set PYTHONPATH
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

# Command to run Alembic migrations and start the application
CMD ["sh", "-c", "/app/db/test_db_migration.sh postgres 5432"]
