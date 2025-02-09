# Install uv
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Change the working directory
WORKDIR /app

# Copy the project files
COPY pyproject.toml /app/
COPY src /app/src/

# Install dependencies and the project in editable mode
RUN uv pip install --system --no-cache -e .

# Expose the port
EXPOSE 8000

# Use python -m to ensure we're using the installed uvicorn
CMD ["python", "-m", "uvicorn", "rhystic.main:app", "--host", "0.0.0.0", "--port", "8000"]