FROM python:3.12-slim

# Environment variables (rarely change)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working dir
WORKDIR /app

# Install system dependencies (rarely change)
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install uv binary
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/


# Copy requirements first
COPY requirements.lock ./requirements.lock

# Install Python dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system -r requirements.lock

# Copy project source last (frequent changes)
COPY . .

# expose port
EXPOSE 8000
# run command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]