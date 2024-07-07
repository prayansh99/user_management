
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir /user_api

# Set the working directory
WORKDIR /user_api

# Copy all the project files to user_api directory
COPY . /user_api/

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && apt-get install -y libpq-dev

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


# Run migrations and start the development server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
