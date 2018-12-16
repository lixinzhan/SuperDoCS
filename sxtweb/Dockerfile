# start from an official image
FROM ubuntu:18.04

# setup environment variables
ENV prj SuperDoCS
ENV ver 2.0-Alpha1

# add packages
RUN apt-get update && \
    apt-get -y install python3 python3-dev python3-django \
                       python3-docutils python3-numpy python3-scipy \
                       python3-xhtml2pdf gunicorn3

# Copy package file
COPY ${prj}_${ver}*.tar.gz /var/www/
WORKDIR /var/www/
RUN tar zxvf ${prj}_${ver}*.tar.gz

# location of the project
WORKDIR /var/www/${prj}_${ver}/

# expose port 8000
EXPOSE 8000

# define the default command to run when starting the container
CMD ["gunicorn3", "--bind", ":8000", "sxtweb.wsgi:application"]

