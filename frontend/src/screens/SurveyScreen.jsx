import React, { useState, useMemo } from 'react';
import { SURVEY_DATA } from '../data/questions';

function SurveyScreen({ onFinish }) {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [collectedAnswers, setCollectedAnswers] = useState([]);

  const allQuestions = useMemo(() => {
    return SURVEY_DATA.flatMap((section) => 
      section.items.map((item) => ({
        ...item,
        category: section.category
      }))
    );
  }, []);

  const handleOptionClick = (option) => {
    const currentQuestion = allQuestions[currentQuestionIndex];
    const newAnswer = { 
      category: currentQuestion.category,
      question_id: currentQuestion.id,
      question_text: currentQuestion.question,
      answer: option 
    };

    const updatedAnswers = [...collectedAnswers, newAnswer];
    setCollectedAnswers(updatedAnswers);

    const nextQuestion = currentQuestionIndex + 1;
    if (nextQuestion < allQuestions.length) {
      setCurrentQuestionIndex(nextQuestion);
    } else {
      onFinish(updatedAnswers);
    }
  };

  const currentQ = allQuestions[currentQuestionIndex];
  const progress = ((currentQuestionIndex + 1) / allQuestions.length) * 100;

  return (
    <div className="survey-screen fade-in">
      <div className="progress-area">
        <div className="progress-header">
          <span className="category-badge">{currentQ.category}</span>
          <span>{currentQuestionIndex + 1} / {allQuestions.length}</span>
        </div>
        <div className="progress-bar-bg">
          <div className="progress-bar-fill" style={{width: `${progress}%`}}></div>
        </div>
      </div>

      <div className="question-area">
        <h2 className="question-text">{currentQ.question}</h2>
      </div>

      <div className="options-grid">
        {currentQ.options.map((option, index) => (
          <button key={index} className="option-card" onClick={() => handleOptionClick(option)}>
            <span className="option-text">{option}</span>
            <div className="check-icon"></div>
          </button>
        ))}
      </div>
    </div>
  );
}

export default SurveyScreen;
