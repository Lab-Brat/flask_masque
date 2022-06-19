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

RUN pwd
RUN ls -l

# Install Python libraries
RUN python3 -m pip install -r Docker/requirements.txt

# Define environmental variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Make entrpoint script executable
RUN chmod +x Docker/entry_point.sh

# configure the container to run in an executed manner
ENTRYPOINT [ "./Docker/entry_point.sh" ]
