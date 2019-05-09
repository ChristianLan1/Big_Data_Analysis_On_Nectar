# Pull base image
FROM python:3.6-slim

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /ccc-assignment2-team69/web_app_django/

# Install dependencies
RUN pip3 install pipenv
COPY Pipfile Pipfile.lock /ccc-assignment2-team69/web_app_django/
COPY requirements.txt /ccc-assignment2-team69/web_app_django/
RUN pipenv install --system
RUN pip3 install -r requirements.txt

# Copy project
COPY . /ccc-assignment2-team69/web_app_django/