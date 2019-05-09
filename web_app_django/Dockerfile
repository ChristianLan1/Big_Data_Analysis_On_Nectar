# Pull base image
FROM python:3.6-slim

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV http_proxy="http://wwwproxy.unimelb.edu.au:8000"
ENV https_proxy="http://wwwproxy.unimelb.edu.au:8000"
ENV ftp_proxy="http://wwwproxy.unimelb.edu.au:8000"
ENV no_proxy=localhost,127.0.0.1,127.0.1.1,ubuntu
# Set work directory
WORKDIR /ccc-assignment2-team69/web_app_django/

# Install dependencies
RUN pip install pipenv
COPY Pipfile Pipfile.lock /ccc-assignment2-team69/web_app_django/
COPY requirements.txt /ccc-assignment2-team69/web_app_django/
RUN pipenv install --system
RUN pip install -r requirements.txt

# Copy project
COPY . /ccc-assignment2-team69/web_app_django/
