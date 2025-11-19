# app/services/embeddings.py
"""
오늘은 실제 임베딩 API 대신, 개발용 더미 임베딩을 사용한다.
텍스트를 해시해서 고정 길이의 float 벡터로 바꾸는 방식이라
항상 같은 텍스트 → 같은 벡터를 반환한다.
"""

import hashlib
from app.core.config import settings


def _hash_to_vector(text: str, dim: int) -> list[float]:
    """
    텍스트를 해시 기반으로 [dim] 길이의 벡터로 변환.
    완전 랜덤은 아니고, 같은 텍스트면 항상 같은 벡터가 나오도록 설계.
    """
    if not text:
        text = " "  # 빈 문자열 방지

    # 기본 해시 시드
    seed = text.encode("utf-8")
    digest = hashlib.sha256(seed).digest()

    floats: list[float] = []
    idx = 0

    # 필요한 차원 수(dim)만큼 반복해서 값 생성
    while len(floats) < dim:
        # digest를 4바이트씩 잘라서 int로 바꾸고, -1.0 ~ 1.0 사이 값으로 정규화
        chunk = digest[idx : idx + 4]
        if len(chunk) < 4:
            # 해시를 한 번 더 갱신해서 바이트 늘리기
            seed = digest
            digest = hashlib.sha256(seed).digest()
            idx = 0
            continue

        int_val = int.from_bytes(chunk, byteorder="big", signed=False)
        # 32비트 최대값으로 나누고 -1~1 사이 값으로 스케일링
        float_val = (int_val / 2**32) * 2.0 - 1.0
        floats.append(float_val)

        idx += 4
        if idx >= len(digest):
            seed = digest
            digest = hashlib.sha256(seed).digest()
            idx = 0

    return floats


def embed_text(text: str) -> list[float]:
    """
    개발용 더미 임베딩 함수.
    settings.EMBEDDING_DIM 차원의 벡터를 반환한다.
    """
    dim = settings.EMBEDDING_DIM
    vec = _hash_to_vector(text, dim)
    return vec