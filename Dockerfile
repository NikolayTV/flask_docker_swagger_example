# pull official base image
FROM python:3.6

COPY . /usr/src/osago_api

# set work directory
WORKDIR /usr/src/osago_api


# Update pip and from requirements.txt install dependencies
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# RUN chmod +x boot.sh
CMD gunicorn -c gunicorn.conf.py wsgi
