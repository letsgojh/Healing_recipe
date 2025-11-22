import google.generativeai as genai
from app.core.config import settings

# Gemini API 키 설정
genai.configure(api_key=settings.GEMINI_API_KEY)

MODEL_NAME = "models/text-embedding-004"  # 최신 임베딩 모델


def embed_text(text: str):
    try:
        result = genai.embed_content(
            model=settings.GEMINI_EMBED_MODEL,
            content=text
        )
        emb = result["embedding"]

        # 기본적인 sanity check
        if len(emb) != 768:
            raise RuntimeError(f"Unexpected embedding dimension: {len(emb)}")

        return emb
    
    except Exception as e:
        print("❌ Embedding API failed:", e)
        raise RuntimeError("Embedding failed. Check GEMINI_API_KEY or network.")