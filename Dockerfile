# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.7

ENV PYTHONUNBUFFERED 1


# create root directory for our project in the container
RUN mkdir /product_service

# Set the working directory to /product_service
WORKDIR /product_service

# Copy the current directory contents into the container at /product_service
ADD . /product_service/

# Install any needed packages specified in requirements.txt
RUN pip3 install -r requirements.txt
