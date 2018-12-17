# start from an official image
FROM ubuntu:18.04

# Information
LABEL maintainer: Lixin Zhan

# setup environment variables
ENV prj SuperDoCS
ENV ver 2.0-Alpha1
ENV prjroot /var/www/SuperDoCS

# add packages
RUN apt-get update && apt-get install -y \
    gunicorn3 \
    python3 \
    python3-django \
    python3-docutils \
    python3-numpy \
    python3-scipy \
    python3-xhtml2pdf \
&& rm -rf /var/lib/apt/lists/*

# Copy package file
ADD ${prj}_${ver}*.tar.gz /var/www/
RUN mv /var/www/${prj}_${ver} ${prjroot}

# expose port 8000
EXPOSE 8000

# volume
VOLUME ["${prjroot}/sxtweb", "${prjroot}/static", "${prjroot}/media", \
        "${prjroot}/config/nginx_conf.d", "${prjroot}/xcalc/UserCodes"]

# location of the project
WORKDIR ${prjroot}

# define the default command to run when starting the container
CMD ["gunicorn3", "--bind", ":8000", "sxtweb.wsgi:application"]

