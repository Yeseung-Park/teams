# Docker 실행 가이드

## 사전 준비

1. Docker와 Docker Compose 설치 확인:
```bash
docker --version
docker-compose --version
```

2. 환경 변수 설정:
```bash
cp .env.example .env
# .env 파일을 열어 필요한 값 수정
```

## 실행 방법

### 전체 스택 실행
```bash
docker-compose up -d
```

### 로그 확인
```bash
docker-compose logs -f
```

### 특정 서비스만 실행
```bash
docker-compose up -d backend
docker-compose up -d frontend
docker-compose up -d db
```

## 접속 정보

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- MySQL: localhost:3306

## 중지 및 정리

### 컨테이너 중지
```bash
docker-compose down
```

### 볼륨까지 삭제 (데이터베이스 초기화)
```bash
docker-compose down -v
```

## 개발 모드

현재 설정은 개발 모드로, 코드 변경 시 자동으로 반영됩니다:
- Backend: uvicorn auto-reload
- Frontend: Vite HMR

## 프로덕션 빌드

프로덕션 환경에서는 별도의 Dockerfile.prod를 생성하여 사용하는 것을 권장합니다.
