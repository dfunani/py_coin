# Use an appropriate base image for your Flask application
FROM python:3.12

# Set the working directory within the container
WORKDIR /app

# Install required packages
RUN apt-get update \
    && apt-get install -y \
    openssh-client \
    git \
    postgresql-client

# Copy the necessary files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
COPY test.env .env
RUN /bin/bash -c "source .env"

# Set PYTHONPATH
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

# Run the migration script
RUN alembic upgrade head

# Start your application (modify as needed)
# CMD ["python", "app.py"]
