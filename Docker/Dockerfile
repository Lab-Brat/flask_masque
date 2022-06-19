# Pull almalinux 8 image
FROM almalinux

# Install dependencies
RUN dnf update -y
RUN dnf install -y gcc libpq-devel postgresql-devel \
                       python3 python3-pip python3-devel

# Copy everything into docker container
COPY . /app

# Switch working directory
WORKDIR /app

# Install Python libraries
RUN python3 -m pip install -r requirements.txt

# Define environmental variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Make entrpoint script executable
RUN chmod +x entry_point.sh

# configure the container to run in an executed manner
ENTRYPOINT [ "./entry_point.sh" ]
