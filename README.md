# LAB

## 개요
이 레포지토리는 다양한 기술 영역의 POC(Proof of Concept)를 위한 실험 장소.
- 하나도 정돈 되어 있지 않음.!

## 주요 영역

### 인프라 (infra)
- [Docker 이미지 최적화 및 Multi-stage build](./infra/lightweight/README.md)
  - [Dockerfile 최적화 전략](./infra/lightweight/README.md)
- [AWS Terraform VPC 생성](./infra/aws-terraform/create_vpc/README.md)

### 프로그래밍
- Go 언어
  - [라우팅 서버 구현](./go-lang/routing/server.go)
  - [시그널 핸들링](./go-lang/signal-handler/main.go)
  - [스택 구현](./go-lang/stack.go)
  - [객체지향 디자인 패턴](./go-lang/composition/main.go)
- Python
  - [AsyncIO 구현](./async/async_python.md)
  - [Makefile 사용 예제](./python/make/README.md)
  - [attrs 라이브러리 활용](./python/attrs/README.md)

### 머신러닝 (ML)
- [sLLM (Small Language Model)](./ML/sLLM/README.md)
  - DPO training with LoRA
  - Quantization 관련 연구

### 디자인 패턴
- [Command Pattern 구현](./design-pattern)

### 데이터
- [Fluent Bit 구현 및 비교 분석](./DE/fluent-bit/README.md)
- [Data 버전 관리](./DE/DVC)
