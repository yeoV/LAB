FROM alpine
LABEL author="LSY" purpose="webserver"
RUN apk update && apk add vim
WORKDIR /var/www/html
COPY index.html .
EXPOSE 80
CMD [ "echo", "Hello World" ]