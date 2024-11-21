FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install Poetry
RUN pip install --no-cache-dir poetry

# Set the working directory
WORKDIR /app

# Copy the project files
COPY pyproject.toml poetry.lock* /app/

# Install dependencies using Poetry
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Copy the FastAPI app
COPY . /app

# Expose the port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "web_scraping_tool.main:app", "--host", "0.0.0.0", "--port", "8000"]
