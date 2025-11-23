# <힐링레시피> - <힐링레시피>

## 서비스 요약
"오늘 하루 지친 당신을 위한 AI 처방전" 사용자의 생활 패턴과 스트레스 성향을 분석하여, 가장 적합한 해소 방법을 추천해주는 맞춤형 멘탈케어 서비스

## 주제 구분
-	S타입 현대인의 스트레스 해소를 위한 서비스 

## 팀원 소개
- 팀명: 힐링레시피
- 이제원
- 유재환
- 박재영
- 박재민

## 시연 영상
https://www.youtube.com/watch?v=vDAqi4s6gCc

## 서비스 소개

### 서비스 개요
힐링레시피는 바쁜 현대인들이 자신의 스트레스 상태를 정확히 인지하고, 이를 건전하게 해소할 수 있도록 돕는 웹 서비스입니다. 사용자는 간단한 설문(수면 시간, 근무 환경, 선호하는 해소 방식 등)을 통해 자신의 스트레스 유형(페르소나)을 진단받습니다. 서비스는 이 데이터를 바탕으로, 단순히 "쉬세요"라는 막연한 조언 대신 "벽 밀기 10회", "종이 찢기" 등 구체적이고 실천 가능한 행동(Recipe)을 처방합니다.

### 타서비스와의 차별점
- 벡터 데이터베이스(Qdrant) 기반의 정교한 매칭: 단순한 키워드 매칭이 아니라, 사용자의 성향과 해결책 사이의 의미적 유사도를 분석하여 가장 적합한 활동을 추천합니다.
- 구체적인 행동 지침(Actionable Item) 제공: 명상이나 음악 감상에 그치지 않고, '행동형', '위로형' 등 유형에 따라 당장 실행할 수 있는 소소하고 구체적인 미션을 제공합니다.
- 직관적이고 반응형인 UI: 모바일 환경에 최적화되어 언제 어디서든 접근 가능하며, PC 환경에서는 넓은 화면을 활용한 몰입감 있는 디자인을 제공합니다.

### 구현 내용 및 결과물
1. 스트레스 유형 진단 설문 시스템
- 수면 시간, 근무 강도, 현재 감정 상태 등 12가지 문항을 통해 사용자 데이터를 수집합니다.
- 프론트엔드에서 수집된 데이터는 백엔드로 전송되어 분석 단계로 넘어갑니다.

2. AI 기반 페르소나 분석 및 솔루션 추천
- 유형 분석: 사용자를 '행동형(Action)', '안정형(Calm)','감각형(Sensation)','정리형(Organize)','사회형(Social)','창의형(Creative)','몰입형(Focus on)','위로형(Comfort)' 8가지 페르소나로 분류하여 현재 상태를 시각적으로 보여줍니다.
- 맞춤 처방: Qdrant 벡터 검색을 통해 수백 가지의 해소 방법 중 사용자에게 가장 효과적인 Top 4 솔루션을 카드 형태로 추천합니다.

### 구현 방식
- Frontend: React, JavaScript, CSS3 (Mobile-First Responsive Design)
- Backend Framework: FastAPI (Python 3.11)
- Vector DB: Qdrant (데이터 영속성 및 고속 유사도 검색)
- AI & Embedding: Google Gemini (text-embedding-004) API 활용
- Data Analysis: Scikit-learn (KMeans Clustering을 통한 페르소나 군집화)
- Infrastructure: Docker & Docker Compose (컨테이너 기반 배포 환경)

### 향후 개선 혹은 발전 방안
- LLM(대형 언어 모델) 도입: 현재의 정해진 추천 목록을 넘어, 사용자의 주관식 고민을 듣고 생성형 AI가 실시간으로 위로의 말을 건네는 챗봇 기능 추가.
- 회원 기능 및 기록 관리: 사용자가 언제 어떤 스트레스를 받았는지 기록하고, 스트레스 변화 추이를 그래프로 보여주는 대시보드 기능 개발.
- 커뮤니티 활성화: 자신만의 스트레스 해소법(레시피)을 다른 사용자와 공유하고 '좋아요'를 누를 수 있는 소셜 기능 확장.
- 벡터 검색 밀도 향상 및 매칭 정교화: 현재의 데이터베이스 규모에서는 임베딩 벡터 간의 거리가 멀어(Sparse), 일부 사용자의 경우 최적의 답변을 찾기 어려운 '콜드 스타트(Cold Start)' 문제가 존재할 수 있습니다. 이를 해결하기 위해 행동 데이터의 수를 늘려 벡터 공간의 밀도를 높이고, KMeans 클러스터링 로직을 세분화하여 추천 정확도를 개선할 예정입니다.

## 실행 방법(MAC 기준)
### 프로젝트 설치
```bash
git clone https://github.com/letsgojh/Healing_recipe.git
cd Healing_recipe/
```
### 환경 변수 설정
백엔드 실행을 위해 API 키 설정이 필요합니다. 프로젝트 폴더(Healing_recipe/healing_recipe)에 ***.env.docker*** 파일을 생성하고 아래 내용을 입력해주세요.<br>
***Note: GEMINI_API_KEY는 Google AI Studio에서 발급받을 수 있습니다.***

```.env.docker
GEMINI_API_KEY=your_google_api_key_here
GEMINI_EMBEDDING_MODEL=models/text-embedding-004
EMBEDDING_DIM=768

QDRANT_HOST=qdrant
QDRANT_PORT=6333
QDRANT_COLLECTION=stress_reliefs
```
### 도커 실행
```bash
docker compose up -d --build
```
### 데이터초기화
```bash
docker compose exec api python -m scripts.load_stress_reliefs
```
### 클러스터링 실행
```bash
docker compose exec api python -m app.services.clustering
```
### 프론트엔드 실행
```bash
cd ../frontend/
npm install
npm install vite
npm run dev
```
