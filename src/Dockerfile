# Python 3.10 in alpine as a basic image
FROM python:3.10-alpine

# Set python to print all output to stdout
ENV PYTHONUNBUFFERED 1

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements.txt file to root dir
COPY requirements.txt .

# Install all dependensies listed in requirements.txt
RUN pip install -r requirements.txt

# Copy src dir content with django app to code dir
COPY . /code

# Change working directory to /code
WORKDIR /code

# Collect static files
RUN python manage.py collectstatic --no-input

############################################ WARNING ############################################
# Due to the migration reasons rest of the code has to be executed in docker compose file