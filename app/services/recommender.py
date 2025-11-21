# app/services/recommender.py

from typing import Any, Dict

import joblib
from qdrant_client import QdrantClient
from sklearn.cluster import KMeans

from app.core.config import settings
from app.services.embeddings import embed_text
from app.services.clustering import StressClusteringService, CLUSTER_SYMBOLS


class StressRecommender:
    """
    사용자 텍스트 → 벡터 → KMeans로 클러스터 예측 → 해당 클러스터 해소법 추천.
    """

    def __init__(
        self,
        collection: str | None = None,
        kmeans_model_path: str = "kmeans_model.pkl",
    ):
        self.collection = collection or settings.QDRANT_COLLECTION

        # QdrantClient는 지금 이 클래스 안에선 직접 안 써도 되지만,
        # 필요할 때를 대비해 남겨둠.
        self.client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT,
        )

        # KMeans 모델 로드
        try:
            self.kmeans: KMeans = joblib.load(kmeans_model_path)
        except Exception:
            raise RuntimeError(
                f"{kmeans_model_path} 파일을 찾을 수 없습니다. "
                "먼저 app/services/clustering.py를 실행해서 모델을 저장하세요."
            )

        # 클러스터 아이템 조회 서비스
        self.cluster_service = StressClusteringService(
            collection_name=self.collection,
        )

    def recommend(self, user_text: str) -> Dict[str, Any]:
        """
        1) 텍스트 임베딩
        2) KMeans.predict()로 사용자 벡터의 클러스터 예측
        3) 해당 클러스터의 해소법 전체 반환
        """
        # 1) 사용자 텍스트 → 벡터
        user_vector = embed_text(user_text)

        # 2) KMeans로 사용자 벡터가 속한 클러스터 예측
        cluster_id = int(self.kmeans.predict([user_vector])[0])

        # 3) 해당 cluster_id의 모든 해소법 가져오기 (payload 리스트)
        items = self.cluster_service.get_cluster_items(cluster_id)

        symbol = CLUSTER_SYMBOLS.get(cluster_id, "UNK - 알 수 없음")

        return {
            "user_text": user_text,
            "cluster_id": cluster_id,
            "symbol": symbol,
            "recommendations": items,
        }


if __name__ == "__main__":
    rec = StressRecommender()
    result = rec.recommend("요즘 머리도 아프고 피곤하고 스트레스가 많아")
    print(result)