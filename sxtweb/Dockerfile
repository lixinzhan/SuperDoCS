# start from an official image
FROM ubuntu:18.04

# Information
LABEL maintainer: Lixin Zhan

# setup environment variables
ENV prj SuperDoCS
ENV ver 2.0-Alpha1
ENV prjroot /var/www/SuperDoCS_2.0-Alpha1

# add packages
RUN apt-get update && \
    apt-get -y install python3 python3-dev python3-django \
                       python3-docutils python3-numpy python3-scipy \
                       python3-xhtml2pdf gunicorn3

# Copy package file
ADD ${prj}_${ver}*.tar.gz /var/www/

# expose port 8000
EXPOSE 8000

# volume
VOLUME ["${prjroot}/sxtweb", "${prjroot}/static", "${prjroot}/media", \
        "${prjroot}/config/nginx_config.d", "${prjroot}/xcalc/UserCodes"]

# location of the project
WORKDIR ${prjroot}

# define the default command to run when starting the container
CMD ["gunicorn3", "--bind", ":8000", "sxtweb.wsgi:application"]

