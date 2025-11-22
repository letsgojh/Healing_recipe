# app/api/v1/recommend.py

from collections import Counter
from typing import List

from fastapi import APIRouter, HTTPException

from app.api.v1.schemas import (
    SurveyAnswers,
    RecommendResponse,
    ReliefItem,
    SymbolResponse,
)
from app.services.profile_builder import build_profile_text
from functools import lru_cache
from app.services.recommender import StressRecommender

router = APIRouter(prefix="/recommend", tags=["recommend"])


@lru_cache
def get_recommender() -> StressRecommender:
    # 처음 한 번만 생성해서 캐시에 넣고, 그 다음부터는 재사용
    return StressRecommender()


@router.post("", response_model=RecommendResponse)
def recommend(answers: SurveyAnswers) -> RecommendResponse:
    """
    설문 응답 → 프로필 텍스트 → Recommender로 추천.
    """

    recommender = get_recommender()

    # 1) 설문 응답을 하나의 설명 텍스트로 변환
    profile_text = build_profile_text(answers)

    # 2) Recommender 호출 (cluster_id + symbol + 추천 리스트 반환)
    result = recommender.recommend(profile_text)

    recommendations = result.get("recommendations", [])
    if not recommendations:
        raise HTTPException(
            status_code=404,
            detail="해당 클러스터에 등록된 스트레스 해소법이 없습니다.",
        )

    # 3) symbol 문자열 파싱 ("ACT - 행동형" → code="ACT", name="행동형")
    raw_symbol = result.get("symbol", "UNK - 알 수 없음")
    if " - " in raw_symbol:
        code, name = raw_symbol.split(" - ", 1)
    else:
        code, name = raw_symbol, raw_symbol

    symbol_resp = SymbolResponse(
        code=code,
        name=name,
        description=(
            f"당신은 '{name}' 성향의 스트레스 해소 유형에 가까운 것으로 보입니다. "
            f"아래 추천 리스트를 참고해 본인에게 맞는 방법을 골라보세요."
        ),
    )

    # 4) 추천 리스트를 ReliefItem으로 변환
    relief_items: List[ReliefItem] = []
    for idx, payload in enumerate(recommendations):
        # payload는 load_dummy_reliefs.py + clustering.py에서 넣어준 딕셔너리라고 가정
        relief_items.append(
            ReliefItem(
                # id는 Qdrant에선 안 가져왔으니, 일단 인덱스로 대체하거나
                # 필요 없으면 schemas에서 id 필드를 optional/nullable로 처리해도 됨
                id=idx,
                title=payload.get("title"),
                description=payload.get("description"),
                persona_label=payload.get("persona_label"),
                cluster_id=payload.get("cluster_id"),
                symbol=payload.get("symbol"),
            )
        )

    return RecommendResponse(
        symbol=symbol_resp,
        reliefs=relief_items,
    )