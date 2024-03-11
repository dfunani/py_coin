# Use an appropriate base image for your Flask application
FROM python:3.10

# Set the working directory within the container
WORKDIR /app

# Install required packages
RUN apt-get update \
    && apt-get install -y \
    openssh-client \
    git \
    postgresql-client

# Set environment variables for Alembic

# COPY requirements.txt .
# COPY /db/test_db_migration.sh .
# COPY alembic.ini .
# Install dependencies

# Run a permissions change on the second script, we'll run.

# Install python dependancies from the requirements.txt file for alembic and psql

COPY . /app

COPY local.env .env

RUN source .env

RUN ./db/test_db_migration.sh

RUN export PYTHONPATH=$PYTHONPATH:$(pwd)

RUN pip install --no-cache-dir -r requirements.txt

