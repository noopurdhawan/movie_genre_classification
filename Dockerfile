# Base image
FROM python:3

# Copy contents
COPY . /app

# Change work directory
WORKDIR /app

# Start the application
CMD ["python", " predict.py"]