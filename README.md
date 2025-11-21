## 🚀 Tech Stack

- **Backend Framework**: FastAPI  
- **Vector DB**: Qdrant  
- **Embedding Model**: Google Gemini (text-embedding-004)  
- **Clustering**: KMeans (scikit-learn)  
- **Containerization**: Docker & Docker Compose  
- **Language**: Python 3.11

## 📂 Project Structure

## 🐳 Run with Docker
### 1) 빌드 & 실행
~~~bash
docker compose up -d --build
~~~

API: http://localhost:8000
Docs(Swagger): http://localhost:8000/docs


## vectorDB
### 스트레스해소법 삽입
~~~bash
docker compose exec api python -m scripts.load_stress_reliefs
~~~
### KMEAN 클러스터링 실행
~~~bash
docker compose exec api python -m app.services.clustering
~~~

## Features
사용자 설문 기반 프로필 텍스트 생성
Gemini 임베딩 → Qdrant 벡터 저장
KMeans 기반 스트레스 유형 분류 (8가지)
맞춤형 해소법 리스트 반환
Swagger UI 제공
Docker 기반 재현 가능한 배포 환경
