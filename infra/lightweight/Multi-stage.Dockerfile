FROM ubuntu:20.04
RUN apt-get update -y && apt-get install nginx -y
COPY appstart.sh /
RUN useradd Kevin
USER Kevin
ENTRYPOINT [ "/appstart.sh" ]