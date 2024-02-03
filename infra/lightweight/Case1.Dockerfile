FROM ubuntu:20.04
LABEL author="LSY" purpose="webserver"
RUN apt update && apt install vim -y &&\
    apt clean autoclean && \
    apt autoremove -y && \
    rm -rfv /tmp/* /var/lib/apt/lists/* /var/tmp/*
WORKDIR /var/www/html
COPY index.html .
EXPOSE 80
CMD [ "echo", "Hello World" ]