# Dockerfile 최적화

- 컨테이너의 경량의 가상화 서비스를 목적으로 함
- base image 들도 해당 이미지의 지향점에 필요한 프로그램, 라이브러리, 실행파일 보장
- **"최소한의 설정과 구성"**
- 최적화 방안

 1. 불필요한 바이너리를 모두 제거
     1. 패키지 파일 autoremove, clean
     2. apt install -y --no-install-recommends -> 불필요한 패키지 방안 접기
     3. .dockerignore 사용해서 빌드와 필요한 파일 이미지 내부에 넣기
 2. 최소 기본 이미지 -> alpine linux , scratch 사용
 3. multi-stage build를 사용하여 최종 이미지 크기를 최소화한다.
     1. 여러개의 base image를 사용한 docker build
     2. 첫 번째 stage에서 생성된 실행파일 등을 두 번째 stage에 제공
 4. Layer 수를 최적화 시켜서 빌드 시간 및 이미지 용량을 최적화 -> 그룹화 하기!
     1. FROM RUN COPY ADD ENV LABEL 적게 사용해라..!
 5. One application One container!
 6. Using cache!
     1. 도커 빌드 시 자동으로 layer 갯수대로 캐싱 됨
     2. 효과를 높이기 위해 명령어 위치 명확히 할 것.
     일정하게 유지될 명령은 Dockerfile 위쪽(패키지 설치 등) 변경될 수 있는 명령은 아래쪽
     3. 보안 강화! -> root 사용자 x, 디지털 서명, 도커에 있는 이미지 스캐너 실행하기, Dive 사용하기

# Docker build

```
docker build -t IMAGE_NAME:TAG DOCKERFILE_LOCATION
```

- `--no-cache` : 캐싱 제거 옵션

- Image로 생성된 layer들은 Read-Only
  - 그렇기 때문에 컨테이너 실행 시, 레이어를 하나 생성해줌

# 경량화 테스트하기

docker build -t light:1.0 -f 파일명 --no-cache .

- Base Image
  - 빌드 시 용량 : 167MB

```
FROM ubuntu:20.04
LABEL author="LSY" purpose="webserver"
RUN apt update && apt install git
WORKDIR /var/www/html
COPY index.html .
EXPOSE 80
CMD [ "apachectl", "-D", "FOREGROUND" ]
```

- Case 1) 패키지 잔여물 제거
  - 빌드 시 용량 : 133MB

```
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
```

- Case 2) alpine 이미지 사용하여 경량화
  - 빌드 시 용량 : 38.7MB

```
FROM alpine
LABEL author="LSY" purpose="webserver"
RUN apk update && apk add vim
WORKDIR /var/www/html
COPY index.html .
EXPOSE 80
CMD [ "echo", "Hello World" ]
```

## Multi-stage build

- 첫번째 이미지
  - 용량 : 158MB

```
FROM ubuntu:20.05
RUN apt-get update -y && apt-get install nginx -y
COPY appstart.sh /
RUN useradd Kevin
USER Kevin
ENTRYPOINT [ "/appstart.sh" ]
```

- 이미지 경량화
- go 언어처럼 빌드될 환경이 있는 경우, Multi-stage 빌드로 가능
  - 용량 : 5.32MB

```
FROM ubuntu:20.04 as v1-stage
RUN apt-get update -y && apt-get install nginx -y
WORKDIR /app
COPY appstart.sh /app

FROM alpine:3.12.1
RUN addgroup -S appgroup && adduser -S kevin -G appgroup -h /home/kevin
COPY --from=v1-stage /app /home/kevin
USER kevin
ENTRYPOINT [ "sh","/home/kevin/appstart.sh" ]
```

# 참고

#### 취약점이 많은 이미지의 경우, Dive 확인 필요

```
docker run --rm -it \
-v /var/run/docker.sock:/var/run/docker.sock \
-v "$(pwd)":"$(pwd)" \
-w "$(pwd)" \
-v "$HOME/.dive.yaml":"$HOME/.dive.yaml" \
wagoodman/dive:latest build -t dive-webapp:1.0 -f dockerfile-myweb2 .
```
