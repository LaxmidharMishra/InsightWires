# Use Python slim image
FROM public.ecr.aws/lambda/python:3.10

COPY ./InsightWires ${LAMBDA_TASK_ROOT}

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for Python
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
#RUN pip install --verbose -r requirements.txt

RUN pip install --no-cache-dir --upgrade pip && \
    pip install awslambdaric
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app/

#RUN CHMOD +x /app/lambda_entry_script.sh
# Expose port for the application
EXPOSE 8000

# Run FastAPI application
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["app.handler"]
#ENTRYPOINT ["/app/lambda_entry_script.sh","main.handler"]