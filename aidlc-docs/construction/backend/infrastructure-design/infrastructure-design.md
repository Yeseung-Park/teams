# Infrastructure Design - Backend

**Unit**: backend
**작성일**: 2026-02-09
**Cloud Provider**: AWS

---

## Infrastructure Mapping

| Logical Component | AWS Service | Configuration |
|-------------------|-------------|---------------|
| Application Server | EC2 | t3.small/medium |
| Database | RDS MySQL | db.t3.micro/small |
| File Storage | S3 | Standard bucket |
| DNS (optional) | Route 53 | - |
| SSL (optional) | ACM | - |

---

## Compute: EC2

### Instance Configuration
| Property | Value |
|----------|-------|
| Instance Type | t3.small (MVP), t3.medium (확장 시) |
| AMI | Amazon Linux 2023 |
| Storage | 20GB gp3 EBS |
| Elastic IP | Yes |

### Security Group (backend-sg)
| Type | Port | Source | Description |
|------|------|--------|-------------|
| Inbound | 22 | My IP | SSH |
| Inbound | 80 | 0.0.0.0/0 | HTTP |
| Inbound | 443 | 0.0.0.0/0 | HTTPS |
| Inbound | 8000 | 0.0.0.0/0 | FastAPI (dev) |
| Outbound | All | 0.0.0.0/0 | All traffic |

---

## Database: RDS MySQL

### Instance Configuration
| Property | Value |
|----------|-------|
| Engine | MySQL 8.0 |
| Instance Class | db.t3.micro (MVP) |
| Storage | 20GB gp2 |
| Multi-AZ | No (MVP) |
| Backup Retention | 7 days |
| Auto Minor Upgrade | Yes |

### Security Group (rds-sg)
| Type | Port | Source | Description |
|------|------|--------|-------------|
| Inbound | 3306 | backend-sg | MySQL from EC2 |

### Parameter Group
- character_set_server: utf8mb4
- collation_server: utf8mb4_unicode_ci

---

## Storage: S3

### Bucket Configuration
| Property | Value |
|----------|-------|
| Bucket Name | table-order-images-{env} |
| Region | ap-northeast-2 |
| Versioning | Disabled |
| Public Access | Block all (presigned URL 사용) |

### Bucket Policy
- EC2 IAM Role에서 PutObject, GetObject 허용

### CORS Configuration
```json
[
  {
    "AllowedOrigins": ["*"],
    "AllowedMethods": ["GET"],
    "AllowedHeaders": ["*"],
    "MaxAgeSeconds": 3600
  }
]
```

---

## IAM

### EC2 Instance Role (table-order-ec2-role)
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::table-order-images-*/*"
    }
  ]
}
```

---

## Network (VPC)

### Default VPC 사용 (MVP)
- Public Subnet에 EC2 배치
- RDS는 같은 VPC 내 배치

### 향후 확장 시
- Private Subnet으로 RDS 이동
- NAT Gateway 추가
- ALB 추가

---

## Cost Estimate (Monthly, ap-northeast-2)

| Service | Configuration | Est. Cost |
|---------|---------------|-----------|
| EC2 | t3.small, 24/7 | ~$15 |
| RDS | db.t3.micro, 24/7 | ~$15 |
| S3 | 10GB storage | ~$0.25 |
| Data Transfer | 10GB/month | ~$1 |
| **Total** | | **~$31/month** |

*Free Tier 적용 시 첫 12개월 무료 또는 할인*
