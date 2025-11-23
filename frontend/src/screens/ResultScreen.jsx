import React from 'react';

function ResultScreen({ name, serverResult, onRestart }) {
  // 1. 데이터가 없을 때 방어 코드
  if (!serverResult) {
    return (
      <div className="result-screen fade-in">
        <div className="error-text">결과를 불러오지 못했습니다.</div>
        <button className="restart-btn" onClick={onRestart}>홈으로 돌아가기</button>
      </div>
    );
  }

  // 2. 구조 분해 할당
  const { symbol, reliefs } = serverResult;

  // 3. 설명 텍스트에서 ** 기호 제거 (깔끔하게 보이도록)
  const cleanDescription = symbol.description.replace(/\*\*/g, '');

  return (
    <div className="result-screen fade-in">
      {/* --- 헤더 섹션: 결과 유형 설명 --- */}
      <div className="result-header">
        <div className="icon-container small">🎉</div>
        
        <div className="header-text">
          <h2>{name}님의 유형은 <span className="highlight">'{symbol.name}'</span></h2>
          <div className="description-box">
            <p>{cleanDescription}</p>
          </div>
        </div>
      </div>

      {/* --- 본문 섹션: 추천 리스트 --- */}
      <div className="recommendation-section">
        <h3>💡 {symbol.name}을 위한 맞춤 처방전</h3>
        
        <div className="cards-grid">
          {reliefs.map((item) => (
            <div key={item.id} className="result-card">
              <div className="card-content">
                <div className="card-icon">💊</div>
                <div className="card-text">
                  <h4>{item.title}</h4>
                  {/* description이 null이면 렌더링 안 함 */}
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