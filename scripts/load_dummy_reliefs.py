# scripts/load_dummy_reliefs.py

import os
import sys

# 프로젝트 루트 추가
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from qdrant_client.models import PointStruct
from app.core.config import settings
from app.services.embeddings import embed_text
from app.services.vectordb import init_collection_if_needed, upsert_reliefs


STRESS_RELIEFS = [
    {
        "title": "혼자 카페에서 조용한 시간 보내기",
        "description": "조용한 카페에서 따뜻한 음료를 마시며 혼자만의 시간을 보내며 생각을 정리해보세요.",
        "persona_label": "QUIET_HEALER",
    },
    {
        "title": "근처 공원에서 가벼운 산책",
        "description": "사람이 적은 시간대에 주변 공원을 천천히 걸으며 몸과 머리를 식혀보세요.",
        "persona_label": "ACTIVE_DRAINER",
    },
    {
        "title": "하루를 정리하는 짧은 저널 쓰기",
        "description": "오늘 있었던 일과 느낀 감정을 짧게라도 적어보면서 머릿속을 정리해보세요.",
        "persona_label": "MIND_PLANNER",
    },
]


def main():
    init_collection_if_needed()

    points: list[PointStruct] = []

    # 👇 enumerate로 1부터 번호 매기기
    for idx, relief in enumerate(STRESS_RELIEFS, start=1):
        text = f"{relief['title']}\n{relief['description']}"
        vec = embed_text(text)

        points.append(
            PointStruct(
                id=idx,  # ✅ Qdrant가 좋아하는 "양의 정수 ID"
                vector=vec,
                payload={
                    "title": relief["title"],
                    "description": relief["description"],
                    "persona_label": relief["persona_label"],
                },
            )
        )

    upsert_reliefs(points)
    print(f"Inserted {len(points)} stress relief items into '{settings.QDRANT_COLLECTION}' collection.")


if __name__ == "__main__":
    main()