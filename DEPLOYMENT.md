# 프로덕션 배포 가이드

## 사전 준비

1. `.env.prod` 파일 수정:
```bash
cp .env.prod .env.production
# .env.production 파일을 열어 강력한 비밀번호로 변경
```

2. 프론트엔드 API URL 설정:
```bash
# frontend/src/services/api.js에서 baseURL을 프로덕션 도메인으로 변경
# 또는 환경 변수 사용
```

## 빌드 및 실행

### 1. 프로덕션 빌드
```bash
docker-compose -f docker-compose.prod.yml build
```

### 2. 실행
```bash
docker-compose -f docker-compose.prod.yml --env-file .env.production up -d
```

### 3. 로그 확인
```bash
docker-compose -f docker-compose.prod.yml logs -f
```

### 4. 중지
```bash
docker-compose -f docker-compose.prod.yml down
```

## 접속

- **Frontend**: http://localhost (포트 80)
- **Backend API**: http://localhost/api/v1
- **API Docs**: http://localhost/api/v1/docs

## 주요 차이점 (개발 vs 프로덕션)

### Frontend
- ✅ Nginx로 정적 파일 서빙
- ✅ 프로덕션 빌드 (최적화)
- ✅ 포트 80 사용

### Backend
- ✅ Non-root 사용자로 실행
- ✅ DEBUG=false
- ✅ 자동 재시작 (restart: always)

### Database
- ✅ 강력한 비밀번호 사용
- ✅ 자동 재시작
- ✅ 데이터 영구 저장 (volume)

## 보안 체크리스트

- [ ] `.env.production` 파일의 모든 비밀번호 변경
- [ ] JWT_SECRET_KEY를 강력한 랜덤 문자열로 변경
- [ ] CORS_ORIGINS를 실제 도메인으로 제한
- [ ] 방화벽 설정 (필요한 포트만 오픈)
- [ ] SSL/TLS 인증서 설정 (HTTPS)

## SSL/TLS 설정 (선택사항)

Let's Encrypt를 사용한 HTTPS 설정:

```bash
# Certbot 설치 및 인증서 발급
# nginx 설정에 SSL 추가
```

## 백업

### 데이터베이스 백업
```bash
docker-compose -f docker-compose.prod.yml exec db mysqldump -uroot -p tableorder > backup.sql
```

### 데이터베이스 복원
```bash
docker-compose -f docker-compose.prod.yml exec -T db mysql -uroot -p tableorder < backup.sql
```

### 이미지 백업
```bash
tar -czf uploads-backup.tar.gz uploads/
```

## 모니터링

### 컨테이너 상태 확인
```bash
docker-compose -f docker-compose.prod.yml ps
```

### 리소스 사용량
```bash
docker stats
```

## 업데이트

```bash
# 코드 업데이트 후
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d
```
