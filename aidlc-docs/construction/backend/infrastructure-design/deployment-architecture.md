# Deployment Architecture - Backend

**Unit**: backend
**작성일**: 2026-02-09

---

## Architecture Diagram

```
                    ┌─────────────────┐
                    │    Internet     │
                    └────────┬────────┘
                             │
                    ┌────────┴────────┐
                    │   Elastic IP    │
                    └────────┬────────┘
                             │
              ┌──────────────┴──────────────┐
              │         EC2 Instance         │
              │  ┌────────────────────────┐  │
              │  │   Nginx (Reverse Proxy) │  │
              │  │        Port 80/443      │  │
              │  └───────────┬────────────┘  │
              │              │               │
              │  ┌───────────┴────────────┐  │
              │  │   Uvicorn + FastAPI    │  │
              │  │       Port 8000        │  │
              │  └───────────┬────────────┘  │
              └──────────────┼──────────────┘
                             │
           ┌─────────────────┼─────────────────┐
           │                 │                 │
    ┌──────┴──────┐   ┌──────┴──────┐   ┌──────┴──────┐
    │  RDS MySQL  │   │   AWS S3    │   │  (Future)   │
    │  Port 3306  │   │   Images    │   │   Redis     │
    └─────────────┘   └─────────────┘   └─────────────┘
```

---

## Deployment Process

### 1. 초기 설정 (1회)

```bash
# EC2 접속
ssh -i key.pem ec2-user@<elastic-ip>

# 시스템 업데이트
sudo yum update -y

# Python 3.11 설치
sudo yum install python3.11 python3.11-pip -y

# Nginx 설치
sudo yum install nginx -y

# 프로젝트 디렉토리 생성
mkdir -p /home/ec2-user/app
```

### 2. 애플리케이션 배포

```bash
# 코드 업로드 (scp 또는 git)
cd /home/ec2-user/app

# 가상환경 생성
python3.11 -m venv venv
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일 편집
```

### 3. 서비스 설정

#### Systemd Service (/etc/systemd/system/fastapi.service)
```ini
[Unit]
Description=FastAPI Table Order Service
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/home/ec2-user/app
Environment="PATH=/home/ec2-user/app/venv/bin"
ExecStart=/home/ec2-user/app/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

#### Nginx Configuration (/etc/nginx/conf.d/fastapi.conf)
```nginx
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_read_timeout 86400;  # SSE 연결 유지
    }
}
```

### 4. 서비스 시작

```bash
# FastAPI 서비스 시작
sudo systemctl enable fastapi
sudo systemctl start fastapi

# Nginx 시작
sudo systemctl enable nginx
sudo systemctl start nginx
```

---

## Environment Variables

```bash
# .env 파일
DATABASE_URL=mysql+aiomysql://user:password@rds-endpoint:3306/tableorder
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRE_HOURS=16
AWS_S3_BUCKET=table-order-images-prod
AWS_REGION=ap-northeast-2
DEBUG=false
CORS_ORIGINS=https://your-domain.com
```

---

## Health Check

### Endpoint
- URL: `GET /health`
- Expected: `200 OK`

### Monitoring (Basic)
```bash
# 서비스 상태 확인
sudo systemctl status fastapi

# 로그 확인
sudo journalctl -u fastapi -f
```

---

## Rollback Procedure

```bash
# 이전 버전으로 롤백
cd /home/ec2-user/app
git checkout <previous-tag>
pip install -r requirements.txt
sudo systemctl restart fastapi
```
