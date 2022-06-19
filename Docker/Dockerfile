# start by pulling the python image
FROM almalinux

RUN dnf update -y
RUN dnf install -y gcc libpq-devel postgresql-devel \
                       python3 python3-pip python3-devel

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN python3 -m pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /app

ENV FLASK_APP=app.py
ENV FLASK_ENV=development

RUN chmod +x entry_point.sh

# configure the container to run in an executed manner
ENTRYPOINT [ "./entry_point.sh" ]

