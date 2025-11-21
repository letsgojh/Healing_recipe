import google.generativeai as genai
from app.core.config import settings

# Gemini API 키 설정
genai.configure(api_key=settings.GEMINI_API_KEY)

MODEL_NAME = "models/text-embedding-004"  # 최신 임베딩 모델


def embed_text(text: str) -> list[float]:
    """
    Gemini Embedding API → 768차원 벡터 반환
    """
    if not isinstance(text, str):
        text = str(text)

    result = genai.embed_content(
        model=MODEL_NAME,
        content=text,
    )

    return result["embedding"]  # float 리스트