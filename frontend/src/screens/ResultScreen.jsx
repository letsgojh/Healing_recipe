import React from 'react';

function ResultScreen({ name, serverResult, onRestart }) {
  if (!serverResult) {
    return (
      <div className="result-screen fade-in">
        <div className="error-text">결과를 불러오지 못했습니다.</div>
        <button className="restart-btn" onClick={onRestart}>홈으로 돌아가기</button>
      </div>
    );
  }

  const { symbol, reliefs } = serverResult;

  const cleanDescription = symbol.description.replace(/\*\*/g, '');

  return (
    <div className="result-screen fade-in">
      <div className="result-header">
        <div className="icon-container small">🎉</div>
        
        <div className="header-text">
          <h2>{name}님의 유형은 <span className="highlight">'{symbol.name}'</span></h2>
          <div className="description-box">
            <p>{cleanDescription}</p>
          </div>
        </div>
      </div>
      <div className="recommendation-section">
        <h3>💡 {symbol.name}을 위한 맞춤 처방전</h3>
        
        <div className="cards-grid">
          {reliefs.map((item) => (
            <div key={item.id} className="result-card">
              <div className="card-content">
                <div className="card-text">
                  <h4>{item.title}</h4>
                  {item.description && <p>{item.description}</p>}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="button-group">
        <button className="restart-btn" onClick={onRestart}>다시 검사하기</button>
      </div>
    </div>
  );
}

export default ResultScreen;