# BUILD STAGE
FROM python:3.11-slim AS builder
RUN apt-get update && apt-get install -y g++ cmake
COPY . /app
WORKDIR /app
RUN pip install .

# PRODUCTION STAGE
FROM python:3.11-slim
WORKDIR /app
ENV PYTHONPATH=/app

# Install runtime dependencies
RUN pip install fastapi uvicorn nltk pytest requests numpy matplotlib bs4 && python -m nltk.downloader stopwords

# Copy the compiled library and dependencies from the builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY . .

# Default command starts the API
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]