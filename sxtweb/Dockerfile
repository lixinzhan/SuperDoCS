# start from an official image
FROM ubuntu:18.04

# add packages
RUN apt-get update
RUN apt-get -y install python3 python3-dev
RUN apt-get -y install python3-django
RUN apt-get -y install python3-docutils
RUN apt-get -y install python3-numpy
RUN apt-get -y install python3-scipy
RUN apt-get -y install python3-xhtml2pdf
RUN apt-get -y install cython3
RUN apt-get -y install gunicorn3

# setup environment variables
ENV prj SuperDoCS
ENV ver 2.0-Alpha1

# Copy package file
COPY SuperDoCS_2.0-Alpha1*.tar.gz /var/www/
WORKDIR /var/www/
RUN tar zxvf SuperDoCS_2.0-Alpha1*.tar.gz

# location of the project
#WORKDIR /var/www/SuperDoCS_2.0-Alpha1/config

# install requirements
#RUN pip3 install -r requirements.txt

# location of the project
WORKDIR /var/www/SuperDoCS_2.0-Alpha1/

# expose port 8000
EXPOSE 8000

# define the default command to run when starting the container
CMD ["gunicorn3", "--bind", ":8000", "sxtweb.wsgi:application"]

