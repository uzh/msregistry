FROM ubuntu:trusty
MAINTAINER Filippo Panessa "filippo.panessa@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN apt-get install -y git
RUN apt-get install -y supervisor
ADD . /opt/msregistry
WORKDIR /opt/msregistry
RUN pip install -r requirements/prod.txt
RUN ln -s /opt/msregistry/conf/supervisor.conf /etc/supervisor/conf.d/
VOLUME ["/opt/msregistry"]
EXPOSE 5000
CMD ["supervisord", "-n"]
