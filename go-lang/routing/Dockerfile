FROM golang:1.23.2 AS builder
WORKDIR /app
COPY . .
RUN go mod download && CGO_ENABLED=0 go build -o mygateway

# stage 2 build
FROM alpine:latest
WORKDIR /app
COPY --from=builder /app/mygateway . 
EXPOSE 8080
ENTRYPOINT [ "./mygateway" ]