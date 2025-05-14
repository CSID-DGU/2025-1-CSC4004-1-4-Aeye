// sidepanel.js: 백그라운드로부터 상품 요약 정보를 수신

var basicInfo =`
    <h2>기본정보</h2>
    <p>제품명, 가격, 배송정보 표시</p>
  `;

var detailInfo = `
    <h2>상세정보</h2>
    <p>보관방법, 주의사항, 특징</p>
  `

var reviewSummary= `
    <h2>리뷰요약</h2>
    <p>리뷰 요약 내용 표시</p>
  `
var currentinfo = "basic";
document.getElementById("btn-basic").addEventListener("click", () => {
  document.getElementById("contentArea").innerHTML = basicInfo;
  currentinfo = "basic";
});

document.getElementById("btn-detail").addEventListener("click", () => {
  document.getElementById("contentArea").innerHTML = detailInfo;
  currentinfo = "detail";
});

document.getElementById("btn-review").addEventListener("click", () => {
  document.getElementById("contentArea").innerHTML = reviewSummary;
  currentinfo = "review";
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

// 메시지 수신 및 데이터 렌더링
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "UPDATE_SIDEPANEL") {
    const contentArea = document.getElementById("contentArea");
   
    // 기본정보 렌더링
     basicInfo = `
      <h2>기본정보</h2>
      <p>상품명: ${message.data.name || '상품명 없음'}</p>
      <p>가격: ${message.data.price || '가격 없음'}</p>
      <p>배송정보: ${message.data.shipping_fee || '배송 정보 없음'}</p>
    `;
  
    // 상세정보 렌더링
    detailInfo = `
      <h2>상세정보</h2>
      <p>옵션정보: ${message.data.more_option || '옵션 없음'}</p>
      <p>평균만족도: ${message.data.average_grade || '평균 평점 없음'}</p>
    `;

    // 리뷰요약 렌더링
    reviewSummary = `
      <h2>리뷰요약</h2>
      <p>리뷰 개수: ${message.data.review_length || '0'}</p>
      <p>대표 리뷰: ${message.data.commentData || '리뷰 없음'}</p>
      <p>부정 리뷰: ${message.data.worstCommentData || '부정 리뷰 없음'}</p>
    `;
    
    if(currentinfo === "basic"){
      contentArea.innerHTML = basicInfo;
    }
    else if(currentinfo === "detail"){
      contentArea.innerHTML = detailInfo;
    }
    else if(currentinfo === "review"){
      contentArea.innerHTML = reviewSummary;
    }
  }
});

