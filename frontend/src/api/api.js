import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000'; 

export const recommend = async (name, age, surveyAnswers) => {
  try {
    const payload = {
      user: {
        name: name,
        age: parseInt(age, 10)
      }
    };
    surveyAnswers.forEach((item, index) => {
      const key = `q${index + 1}`;
      const value = `${item.question_text}: ${item.answer}`; 
      
      payload[key] = value;
    });
    const response = await axios.post(`${API_BASE_URL}/api/v1/recommend`, payload);
    return response.data;

  } catch (error) {
    console.error("API 호출 에러:", error);
    throw error; 
  }
};