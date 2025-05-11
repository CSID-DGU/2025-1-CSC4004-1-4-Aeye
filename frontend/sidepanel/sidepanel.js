// sidepanel.js: 백그라운드로부터 상품 요약 정보를 수신
document.getElementById("btn-basic").addEventListener("click", () => {
  document.getElementById("contentArea").innerHTML = `
    <h2>기본정보</h2>
    <p>제품명, 가격, 배송정보 표시</p>
  `;
});

document.getElementById("btn-detail").addEventListener("click", () => {
  document.getElementById("contentArea").innerHTML = `
    <h2>상세정보</h2>
    <p>보관방법, 주의사항, 특징</p>
  `;
});

document.getElementById("btn-review").addEventListener("click", () => {
  document.getElementById("contentArea").innerHTML = `
    <h2>리뷰요약</h2>
    <p>리뷰 요약 내용 표시</p>
  `;
});

// 큰 글씨 버튼 기능 
let isLargeFont = false;

document.getElementById("btn-font").addEventListener("click", () => {
  const content = document.getElementById("contentArea");
  if (!isLargeFont) {
    content.style.fontSize = "1.5em";
  } else {
    content.style.fontSize = "1em";
  }
  isLargeFont = !isLargeFont;
});

// 스피커 버튼 기능 
document.getElementById("btn-speak").addEventListener("click", () => {
  const text = document.getElementById("contentArea").innerText;
  const utterance = new SpeechSynthesisUtterance(text);  // 읽을 텍스트를 담은 음성 객체 생성 
  speechSynthesis.speak(utterance); //웹브라우저에 내장된 음성합성 기능으로 텍스트 읽기 
});

