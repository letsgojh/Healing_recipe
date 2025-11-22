# Dockerfile

FROM python:3.11-slim

# 컨테이너 안 작업 디렉토리
WORKDIR /app

# 시스템 필수 패키지 (필요시 추가)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 파이썬 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트 소스 복사
COPY . .

# uvicorn으로 FastAPI 실행
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]