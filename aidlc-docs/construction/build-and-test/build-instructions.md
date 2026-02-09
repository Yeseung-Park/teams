# Build Instructions

## Prerequisites

### Backend
- Python 3.11+
- pip
- MySQL 8.0 (또는 Docker)

### Frontend
- Node.js 18+
- npm

### Environment Variables
```bash
# Backend (.env)
DATABASE_URL=mysql+aiomysql://user:password@localhost:3306/tableorder
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRE_HOURS=16
AWS_S3_BUCKET=your-bucket
AWS_REGION=ap-northeast-2
DEBUG=true
CORS_ORIGINS=*
```

---

## Build Steps

### 1. Backend Setup

```bash
cd backend

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일 편집하여 실제 값 입력
```

### 2. Database Setup

```bash
# MySQL 접속
mysql -u root -p

# 데이터베이스 생성
CREATE DATABASE tableorder CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'tableorder'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON tableorder.* TO 'tableorder'@'localhost';
FLUSH PRIVILEGES;
```

### 3. Frontend Setup

```bash
cd frontend

# 의존성 설치
npm install
```

---

## Run Development Servers

### Backend
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm run dev
```

---

## Production Build

### Backend
```bash
cd backend
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend
```bash
cd frontend
npm run build
# dist/ 폴더에 빌드 결과물 생성
```

---

## Verify Build Success

### Backend
- `http://localhost:8000/health` 접속 시 `{"status": "healthy"}` 응답
- `http://localhost:8000/docs` 에서 Swagger UI 확인

### Frontend
- `http://localhost:3000` 접속 시 로그인 화면 표시
- 개발자 도구 콘솔에 에러 없음

---

## Troubleshooting

### Backend: ModuleNotFoundError
```bash
pip install -r requirements.txt
```

### Backend: Database Connection Error
- MySQL 서비스 실행 확인
- DATABASE_URL 환경 변수 확인
- 데이터베이스 및 사용자 권한 확인

### Frontend: npm install 실패
```bash
rm -rf node_modules package-lock.json
npm install
```

### Frontend: Vite proxy 오류
- Backend 서버가 8000 포트에서 실행 중인지 확인
- vite.config.js의 proxy 설정 확인
