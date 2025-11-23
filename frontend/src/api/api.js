import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000'; // 본인 환경에 맞게 수정

export const recommend = async (name, age, surveyAnswers) => {
  try {
    // 1. 기본 payload 구조 생성
    const payload = {
      user: {
        name: name,
        age: parseInt(age, 10)
      }
      // 여기에 q1 ~ q12가 추가될 예정
    };

    // 2. surveyAnswers 배열을 순회하며 q1 ~ q12 필드 동적 생성
    // surveyAnswers[0] -> q1, surveyAnswers[1] -> q2 ... 식
    surveyAnswers.forEach((item, index) => {
      const key = `q${index + 1}`; // q1, q2, q3... 생성
      
      // 요구사항 포맷: "질문 텍스트: 사용자가 고른 답"
      const value = `${item.question_text}: ${item.answer}`; 
      
      payload[key] = value;
    });

    // (디버깅용) 실제로 어떻게 날아가는지 콘솔에서 확인해보세요
    console.log("🚀 서버로 전송되는 Payload:", JSON.stringify(payload, null, 2));

    // 3. POST 요청 전송
    const response = await axios.post(`${API_BASE_URL}/api/v1/recommend`, payload);
    
    return response.data;

  } catch (error) {
    console.error("API 호출 에러:", error);
    throw error; 
  }
};