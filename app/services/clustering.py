# app/services/clustering.py

from typing import List, Tuple
from app.core.config import settings
from qdrant_client import QdrantClient
from qdrant_client.http import models as rest
from sklearn.cluster import KMeans
import joblib

CLUSTER_SYMBOLS = {
    0: "ACT - 행동형",
    1: "CAL - 안정형",
    2: "SEN - 감각형",
    3: "ORG - 정리형",
    4: "SOC - 사회형",
    5: "CRE - 창의형",
    6: "FUN - 몰입형",
    7: "COM - 위로형",
}


class StressClusteringService:
    def __init__(
        self,
        collection_name: str | None = None,
        host: str | None = None,
        port: int | None = None,
    ):
        self.collection = collection_name or settings.QDRANT_COLLECTION
        self.client = QdrantClient(
            host=host or settings.QDRANT_HOST,
            port=port or settings.QDRANT_PORT,
        )

    def _fetch_all_vectors(self) -> Tuple[List[List[float]], List[str]]:
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
        vectors, ids = self._fetch_all_vectors()

        if len(vectors) < n_clusters:
            raise ValueError("벡터 개수보다 클러스터 개수가 많습니다.")

        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        labels = kmeans.fit_predict(vectors)

        # 🔹 여기서 컨테이너 안에 kmeans_model.pkl 생성
        joblib.dump(kmeans, "kmeans_model.pkl")

        # Qdrant payload에 cluster_id / symbol 저장
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
        scroll 전체 돌면서 cluster_id 매칭되는 payload만 수집
        """
        matched = []
        offset = None

        while True:
            batch, offset = self.client.scroll(
                collection_name=self.collection,
                limit=100,
                offset=offset,
                with_payload=True,
                with_vectors=False,
            )

            for p in batch:
                if p.payload.get("cluster_id") == cluster_id:
                    matched.append(p.payload)

            if offset is None:
                break

        return matched

if __name__ == "__main__":
    service = StressClusteringService()
    labels = service.cluster(8)
    print("클러스터링 완료. 라벨 개수:", len(labels))