FROM ubuntu:20.04 as v1-stage
RUN apt-get update -y && apt-get install nginx -y
WORKDIR /app
COPY appstart.sh /app

FROM alpine:3.12.1
RUN addgroup -S appgroup && adduser -S kevin -G appgroup -h /home/kevin
COPY --from=v1-stage /app /home/kevin
USER kevin
ENTRYPOINT [ "sh","/home/kevin/appstart.sh" ]