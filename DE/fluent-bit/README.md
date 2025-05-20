# Fluent Bit

Fluent Bit는 고성능 로그 처리 및 전송 도구
- docs: [Fluent Bit](https://docs.fluentbit.io/manual/)

## Install

- Docker
- debug 이미지 -> CLI, Sh 등 디버깅을 위한 용도
``` bash
docker run -it --rm --name fluentbit-test \
-p 24225:24225 -v ./fluent-bit.conf:/fluent-bit/etc/fluent-bit.conf \
cr.fluentbit.io/fluent/fluent-bit:4.0.1-debug
```

## conf 파일
- filter 기능, Lua 를 활용하면 더 다양한 기능 구현 가능

## 예제

- [소스코드](./fluent-bit.conf)
- Tag 값을 통해서 input output routing 함
- ${es_index} 와 같은 변수 사용 가능 (환경변수, 동적 변수는 사용 어려움 -> 해결 어떻게??)


```yaml
[SERVICE]   # 서비스 전반적인 설정
    log_level debug

[INPUT]     # 입력 설정, Tag 나 tag_key에 대한 개념
    Name http
    Listen 0.0.0.0
    Port 24225
    tag_key es_index

[OUTPUT]
    Name stdout
    Match *

[OUTPUT]
    Name es
    Match *
    Host host.docker.internal
    Port 9200
    Index ${es_index}
    Http_User ${es_user}
    Http_Passwd ${es_password}
    Generate_ID true
    tls On
    tls.verify Off   # self signed cert
    Trace_Output true
    Suppress_Type_Name On  # ES 8.0 이상
```

## vs filebeat
gpt 답변이라 정확하지 않을 수도

> Fluent Bit ＝ 초경량·플러그인·다중 출력·고급 필터 → 컨테이너·엣지·멀티 클라우드
> Filebeat ＝ Elastic Stack 일체형·모듈 템플릿·쉬운 운용 → “ES만 쓴다” 환경

**-> 내 생각 : 다양한 채널을 지원하고 사이드카 패턴의 리소스 적은 Edge Collector가 필요할 경우, fluent-bit이 더 적합하지 않을까..?**

- Fluent Bit이 더 적합할까?
  - 컨테이너 사이드카 — 메모리 < 50 MB, 초경량 수집기 필요
  - Elasticsearch 외 다중 출력 (Kafka, S3, Loki 등) 를 동시에 써야 함
  - 로그 변환·마스킹·라우팅 같은 복잡한 파이프가 필요
  - Fluentd → Fluent-Bit 로 통합하려는 CNCF 표준 스택

- Filebeat이 더 편할까?
  - Elastic Stack 전용 — Kibana 대시보드·ILM·Module 템플릿 즉시 활용
  - Nginx, MySQL, System 로그 등 Beat Module 로 1-클릭 파서·대시보드 요구
  - 기존 ECK/Elastic-Cloud 환경·라이선스 정책에 맞춰야 할 때
  - 디스크 Queue 중심의 대량 로그 안정 수집 선호 (Logstash 파이프 포함)
