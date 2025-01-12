FROM python:3.10-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the working directory
WORKDIR /app

COPY . .

# Install the dependencies
RUN uv sync

# Expose the port
EXPOSE 80
