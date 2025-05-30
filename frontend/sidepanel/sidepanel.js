// sidepanel.js: 백그라운드로부터 상품 요약 정보를 수신

// goole TTS API 키 
const GOOGLE_TTS_KEY = "AIzaSyCyzM_BISF7DF2cBsLwe-OB4nnUAFjEUnc";
const REGION_ENDPOINT = "https://asia-southeast1-texttospeech.googleapis.com";

async function gTTS(text, voice = 'ko-KR-Chirp3-HD-Leda') {

  const body = {
    input: { text },
    voice: { languageCode: 'ko-KR', name: voice},
    audioConfig: { audioEncoding: 'MP3' }
  };

  const res = await fetch(
    `${REGION_ENDPOINT}/v1/text:synthesize?key=${GOOGLE_TTS_KEY}`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    }
  );

  const { audioContent } = await res.json();

  const audio = new Audio(`data:audio/mp3;base64,${audioContent}`);
  await audio.play();
}

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
document.getElementById("btn-font").addEventListener("click", () => {
  const content = document.getElementById("contentArea");
  content.classList.toggle("large-font");
});



// 스피커 버튼 기능 
document.getElementById("btn-speak").addEventListener("click", async () => {
  const text = document.getElementById("contentArea").innerText;
  
  try {
    await gTTS(text);    // WaveNet/Neural 음성
  } catch (e) {
    console.error("GCP TTS 실패, 기본 음성으로 폴백");
    const u = new SpeechSynthesisUtterance(text);
    speechSynthesis.speak(u);         // 로컬 TTS 백업
  }
});


// 메시지 수신 및 데이터 렌더링
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "updateSidepanel") {
    const contentArea = document.getElementById("contentArea");
   
    // 기본정보 렌더링
     basicInfo = `
      <div class="info-block">
        <div class="label">📦 상품명</div>
        <div class="value"> ${message.data.name || '상품명 없음'}</div>
      </div>
      <div class="info-block">
        <div class="label">💰 가격</div>
        <div class="value"> ${message.data.price || '가격 없음'}</div>
      </div>
      <div class="info-block">
        <div class="label">🚚 배송정보</div>
        <div class="value"> ${message.data.shipping_fee || '배송 정보 없음'}</div>
      </div>
    `;

    // 상세정보 렌더링
    detailInfo = `
      <div class="info-block">
        <div class="label">🧾 옵션 정보</div>
        <div class="value"> ${message.data.detailed_info || '옵션 없음'}</div>
      </div>
    `;

    // 리뷰요약 렌더링
    reviewSummary = `
      <div class="info-block">
        <div class="label">📝 리뷰 개수</div>
        <div class="value"> ${message.data.review_length || '0'}</div>
      </div>
      <div class="info-block">
        <div class="label">📜 리뷰 정보</div>
        <div class="value"> ${message.data.review_all || '리뷰 정보 없음'}</div>
      </div>
      <div class="info-block">
        <div class="label">👍 대표 리뷰</div>
        <div class="value"> ${message.data.comment_data || '리뷰 없음'}</div>
      </div>
      <div class="info-block">
        <div class="label">⭐ 평균 만족도</div>
        <div class="value"> ${message.data.average_grade || '평균 평점 없음'}</div>
      </div>

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