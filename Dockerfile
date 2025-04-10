FROM python:3.10

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install pandas sqlalchemy psycopg2 pyarrow

# Set working directory
WORKDIR /app

# Copy script
COPY ingest_data.py ingest_data.py

# Define entrypoint
ENTRYPOINT ["python", "ingest_data.py"]
