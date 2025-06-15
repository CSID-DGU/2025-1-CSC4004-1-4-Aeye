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
    <p>
      <img id="loading" src="https://i.gifer.com/ZZ5H.gif" alt="로딩 중..." /><br>
      제품의 기본 정보를 요약하는 중입니다...
    </p>
  `;

var detailInfo = `
    <p>
      <img id="loading" src="https://i.gifer.com/ZZ5H.gif" alt="로딩 중..." /><br>
      제품의 상세 정보를 요약하는 중입니다...
    </p>
  `;

var reviewSummary= `
    <p>
      <img id="loading" src="https://i.gifer.com/ZZ5H.gif" alt="로딩 중..." /><br>
      제품의 리뷰 정보를 요약하는 중입니다...
    </p>
  `;
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
  (async () => {
    const contentArea = document.getElementById("contentArea");
    try {
      if (message.action === "BASIC_SUMMARY_RESULT") {
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
      } else if (message.action === "DETAIL_SUMMARY_RESULT") {
        detailInfo = `
          <div class="info-block">
            <div class="label">🧾 세부 정보</div>
            <div class="value"> ${message.data.detail || '세부정보 없음'}</div>
          </div>
        `;
      } else if (message.action === "REVIEW_SUMMARY_RESULT") {
        reviewSummary = `
          <div class="info-block">
            <div class="label">📝 리뷰 개수</div>
            <div class="value"> ${message.data.review_count || '0'}</div>
          </div>
          <div class="info-block">
            <div class="label">📜 리뷰 정보</div>
            <div class="value"> ${message.data.review_info || '리뷰 정보 없음'}</div>
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
      } else {
        // 처리할 메시지가 아니면 종료
        return;
      }

      // 현재 탭에 맞는 정보 렌더링
      if (currentinfo === "basic") {
        contentArea.innerHTML = basicInfo;
      } else if (currentinfo === "detail") {
        contentArea.innerHTML = detailInfo;
      } else if (currentinfo === "review") {
        contentArea.innerHTML = reviewSummary;
      }

      // 필요하다면 sendResponse 호출
      // sendResponse({ status: "ok" });
    } catch (e) {
      console.error("메시지 처리 중 오류:", e);
      // sendResponse({ status: "error", error: e.toString() });
    }
  })();

  // 비동기 처리를 위해 true 반환
  return true;
});