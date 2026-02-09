# Table Order Service - Backend

테이블오더 서비스 백엔드 API 서버

## Tech Stack

- Python 3.11+
- FastAPI
- SQLAlchemy 2.0 (async)
- MySQL 8.0
- JWT Authentication
- AWS S3 (이미지 저장)

## Setup

### 1. 가상환경 생성

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정

`.env` 파일 생성:

```env
DATABASE_URL=mysql+aiomysql://user:password@localhost:3306/tableorder
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRE_HOURS=16
AWS_S3_BUCKET=your-bucket
AWS_REGION=ap-northeast-2
DEBUG=true
CORS_ORIGINS=*
```

### 4. 데이터베이스 생성

```sql
CREATE DATABASE tableorder CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. 서버 실행

```bash
uvicorn app.main:app --reload --port 8000
```

## API Documentation

서버 실행 후:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Customer
- `POST /api/v1/auth/customer/login` - 테이블 로그인
- `GET /api/v1/customer/menus` - 메뉴 조회
- `POST /api/v1/customer/orders` - 주문 생성
- `GET /api/v1/customer/orders` - 주문 내역 조회

### Admin
- `POST /api/v1/auth/admin/login` - 관리자 로그인
- `GET /api/v1/admin/orders/stream` - 실시간 주문 (SSE)
- `GET /api/v1/admin/orders` - 활성 주문 조회
- `PATCH /api/v1/admin/orders/{id}/status` - 주문 상태 변경
- `DELETE /api/v1/admin/orders/{id}` - 주문 삭제
- `POST /api/v1/admin/tables/{id}/complete` - 테이블 이용 완료
- `GET /api/v1/admin/tables/{id}/history` - 과거 내역 조회
- `GET /api/v1/admin/menus` - 메뉴 조회
- `POST /api/v1/admin/menus` - 메뉴 등록
- `PUT /api/v1/admin/menus/{id}` - 메뉴 수정
- `DELETE /api/v1/admin/menus/{id}` - 메뉴 삭제
- `POST /api/v1/admin/upload/image` - 이미지 업로드

## Testing

```bash
pytest tests/ -v
```

## Project Structure

```
backend/
├── app/
│   ├── auth/          # 인증
│   ├── menu/          # 메뉴 관리
│   ├── order/         # 주문 관리
│   ├── table/         # 테이블 관리
│   ├── upload/        # 파일 업로드
│   ├── sse/           # 실시간 이벤트
│   ├── models/        # DB 모델
│   ├── core/          # 설정, DB, 의존성
│   └── main.py
├── tests/
├── requirements.txt
└── README.md
```
