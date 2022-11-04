# Pull almalinux 8 image
# FROM almalinux:9.0
FROM python:3.10-slim

# Install dependencies
RUN apt-get update
RUN apt-get install -y libpq-dev gcc

# Copy everything into docker container and cd
COPY . /app
WORKDIR /app

# Install Python libraries
RUN python3 -m pip install -r Docker/requirements.txt

# Define environmental variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Make entrpoint script executable
RUN chmod +x Docker/entry_point.sh

# configure the container to run in an executed manner
ENTRYPOINT [ "Docker/./entry_point.sh" ]
