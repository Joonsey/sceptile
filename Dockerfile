# Use the official Python image from the Docker Hub
FROM python:3.11-slim-buster

# Set the working directory in the container
WORKDIR /app

COPY . /app

RUN pip install poetry

RUN poetry install --no-root --only main

RUN poetry run python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Make port 5555 available to the world outside this container
EXPOSE 5555

# Run zmq_server.py when the container launches
CMD ["poetry", "run", "python", "server.py"]
