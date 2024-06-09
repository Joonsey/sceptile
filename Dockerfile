# Use the official Python image from the Docker Hub
FROM python:3.11-slim-buster

# Set the working directory in the container
WORKDIR /app

COPY pyproject.toml poetry.lock /app/

run pip install poetry

# Install the ZeroMQ library
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Copy the current directory contents into the container at /app
COPY model /app
COPY out /app
COPY server.py /app

# Make port 5555 available to the world outside this container
EXPOSE 5555

# Run zmq_server.py when the container launches
CMD ["poetry", "run", "python", "server.py"]
