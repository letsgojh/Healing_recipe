import google.generativeai as genai
from app.core.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

def explain_symbol(code: str, name: str) -> str:
    prompt = f"""
    스트레스 해소 성향 '{name}'({code})에 대해
    2~4문장으로 간단하고 쉽게 설명해줘.
    """

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        res = model.generate_content(prompt)

        # 응답이 비어있는 경우 방지
        if not hasattr(res, "text") or not res.text:
            return "이 성향에 대한 설명을 불러오지 못했습니다."

        return res.text.strip()

    except Exception as e:
        # 로깅도 가능
        print("Gemini error:", e)
        return "이 성향에 대한 설명을 가져오는 중 문제가 발생했습니다."