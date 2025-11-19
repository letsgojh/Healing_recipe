# app/services/vectordb.py

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from qdrant_client.models import PointStruct
from app.core.config import settings

# 임베딩 차원: config에서 가져옴
VECTOR_DIM = settings.EMBEDDING_DIM

client = QdrantClient(
    host="localhost",
    port=6333,
)


def init_collection_if_needed():
    """
    컬렉션이 없으면 생성. 있으면 아무 것도 안 함.
    """
    collections = client.get_collections().collections
    names = [c.name for c in collections]

    if settings.QDRANT_COLLECTION not in names:
        client.create_collection(
            collection_name=settings.QDRANT_COLLECTION,
            vectors_config=VectorParams(
                size=VECTOR_DIM,
                distance=Distance.COSINE,
            ),
        )
        print(f"[Qdrant] Created collection: {settings.QDRANT_COLLECTION}")
    else:
        print(f"[Qdrant] Collection already exists: {settings.QDRANT_COLLECTION}")


def upsert_reliefs(points: list[PointStruct]):
    """
    해소법(PointStruct 리스트)을 upsert.
    팀원이 사용할 스크립트에서 이 함수를 호출해도 되고,
    지금은 간단한 테스트용으로 쓸 수도 있다.
    """
    client.upsert(
        collection_name=settings.QDRANT_COLLECTION,
        points=points,
        wait=True,
    )


def search_similar_stress_reliefs(query_vector: list[float], top_k: int = 10):
    """
    쿼리 벡터와 가장 가까운 해소법들을 검색.
    payload에 title, description, persona_label 이 들어있다고 가정.
    """
    results = client.search(
        collection_name=settings.QDRANT_COLLECTION,
        query_vector=query_vector,
        limit=top_k,
        with_payload=True,
    )
    return results