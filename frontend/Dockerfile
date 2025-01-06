# FROM python:3.10-slim

# # Install system dependencies for PostgreSQL
# RUN apt-get update && apt-get install -y \
#     gcc \
#     libpq-dev \
#     && rm -rf /var/lib/apt/lists/*

# WORKDIR /app

# # Install Python dependencies
# RUN pip install --no-cache-dir fastapi uvicorn asyncpg sqlalchemy

# COPY . .

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]

FROM nginx:alpine
COPY ./index.html /usr/share/nginx/html/index.html
