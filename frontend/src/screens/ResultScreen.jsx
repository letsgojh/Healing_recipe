import React from 'react';

function ResultScreen({ name, serverResult, onRestart }) {
  if (!serverResult) {
    return (
      <div className="result-screen fade-in">
        <div className="error-text">분석 결과가 없습니다. 다시 시도해주세요.</div>
        <button className="restart-btn" onClick={onRestart}>홈으로 돌아가기</button>
      </div>
    );
  }

  const { symbol, reliefs } = serverResult;

  return (
    <div className="result-screen fade-in">
      <div className="result-header">
        <div className="icon-container small">🎁</div> 
        
        <div className="header-text">
          <h2>{name}님은 <span className="highlight">'{symbol.name}'</span> 입니다</h2>
          <p className="symbol-desc">{symbol.description}</p>
        </div>
      </div>

      <div className="recommendation-section">
        <h3>✨ {name}님을 위한 추천 레시피</h3>
        
        <div className="cards-grid">
          {reliefs.map((item) => (
            <div key={item.id} className="result-card">
              <div className="card-header">
                <div className="card-icon-box">💊</div>
                <div className="card-title-box">
                    <h3>{item.title}</h3>
                    {item.description && <p>{item.description}</p>}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <button className="restart-btn" onClick={onRestart}>다시 검사하기</button>
    </div>
  );
}

export default ResultScreen;