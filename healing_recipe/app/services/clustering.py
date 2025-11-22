# app/services/clustering.py

from typing import List, Tuple
from app.core.config import settings
from qdrant_client import QdrantClient
from qdrant_client.http import models as rest
from sklearn.cluster import KMeans
import joblib


CLUSTER_SYMBOLS = {
    0: "ACT - 행동형",    # 운동, 활동, 움직임
    1: "CAL - 안정형",    # 명상, 휴식
    2: "SEN - 감각형",    # 향, 소리, 감각 자극
    3: "ORG - 정리형",    # 환경 정돈, 청소
    4: "SOC - 사회형",    # 대화, 소통
    5: "CRE - 창의형",    # 그림, 요리, DIY
    6: "FUN - 몰입형",    # 게임, 퍼즐, 플로우
    7: "COM - 위로형",    # 음식, 따뜻한, comfort
}


class StressClusteringService:
    def __init__(
        self,
        collection_name: str | None = None,
        host: str | None = None,
        port: int | None = None,
    ):
        """
        host/port를 명시하면 그걸 우선 사용,
        아니면 settings(QDRANT_HOST/PORT)를 사용.
        """
        self.collection = collection_name or settings.QDRANT_COLLECTION
        self.client = QdrantClient(
            host=host or settings.QDRANT_HOST,
            port=port or settings.QDRANT_PORT,
        )

    def _fetch_all_vectors(self) -> Tuple[List[List[float]], List[str]]:
        """
        Qdrant 컬렉션의 모든 벡터와 ID를 가져온다.
        """
        points, _ = self.client.scroll(
            collection_name=self.collection,
            limit=10000,
            with_vectors=True,
            with_payload=True,
        )

        vectors = [p.vector for p in points]
        ids = [p.id for p in points]

        return vectors, ids

    def cluster(self, n_clusters: int = 8) -> List[int]:
        """
        전체 벡터를 KMeans로 클러스터링하고
        cluster_id & symbol을 Qdrant payload에 저장한다.
        """
        vectors, ids = self._fetch_all_vectors()

        if len(vectors) < n_clusters:
            raise ValueError("벡터 개수보다 클러스터 개수가 많습니다.")

        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        labels = kmeans.fit_predict(vectors)

        # KMeans 모델 저장
        joblib.dump(kmeans, "kmeans_model.pkl")

        # 각 포인트에 cluster_id + symbol 저장
        for pid, cluster_id in zip(ids, labels):
            symbol = CLUSTER_SYMBOLS.get(int(cluster_id), "?")
            self.client.set_payload(
                collection_name=self.collection,
                points=[pid],
                payload={
                    "cluster_id": int(cluster_id),
                    "symbol": symbol,
                },
            )

        return labels

    def get_cluster_items(self, cluster_id: int):
        """
        특정 cluster_id에 속한 항목들의 payload를 반환.
        """
        result, _ = self.client.scroll(
            collection_name=self.collection,
            scroll_filter=rest.Filter(
                must=[
                    rest.FieldCondition(
                        key="cluster_id",
                        match=rest.MatchValue(value=cluster_id),
                    )
                ]
            ),
            with_payload=True,
            with_vectors=False,
        )

        return [p.payload for p in result]


if __name__ == "__main__":
    service = StressClusteringService()
    labels = service.cluster(8)
    print("클러스터링 완료. 라벨 개수:", len(labels))