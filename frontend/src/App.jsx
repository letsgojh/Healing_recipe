import React, { useState } from 'react';
import './App.css';
import StartScreen from './screens/StartScreen';
import SurveyScreen from './screens/SurveyScreen';
import ResultScreen from './screens/ResultScreen';
import { recommend } from './api/api';

function App() {
  const [step, setStep] = useState('start'); 
  const [name, setName] = useState('');
  const [age, setAge] = useState('');
  
  const [isLoading, setIsLoading] = useState(false);
  const [serverResult, setServerResult] = useState(null); 

  const handleStart = () => {
    if (name && age) setStep('survey');
    else alert('이름과 나이를 입력해주세요.');
  };

  const handleSurveyFinish = async (collectedAnswers) => {
    setIsLoading(true);
    
    try {
      const result = await recommend(name, age, collectedAnswers);
      setServerResult(result);
      setStep('result');
      
    } catch (error) {
      alert("서버 연결에 실패했습니다.");
      console.error(error);

      setStep('result'); 
    } finally {
      setIsLoading(false);
    }
  };

  const handleRestart = () => {
    setStep('start');
    setName('');
    setAge('');
    setServerResult(null);
    setIsLoading(false);
  };

  return (
    <div className="app-container">
      {isLoading && (
        <div className="loading-overlay fade-in">
          <div className="spinner"></div>
          <p>== AI가 당신의 스트레스를 분석하고 있습니다 ==</p>
        </div>
      )}

      <div className={`content-box ${step}`}>
        
        {step === 'start' && (
          <StartScreen 
            name={name} 
            setName={setName} 
            age={age} 
            setAge={setAge} 
            onStart={handleStart} 
          />
        )}

        {step === 'survey' && (
          <SurveyScreen 
            onFinish={handleSurveyFinish} 
          />
        )}

        {step === 'result' && (
          <ResultScreen 
            name={name}
            serverResult={serverResult}
            onRestart={handleRestart} 
          />
        )}

      </div>
    </div>
  );
}

export default App;
