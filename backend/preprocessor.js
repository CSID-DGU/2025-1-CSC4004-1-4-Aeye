export function cleanText(rawText){
  let cleaned=rawText;
  cleaned=cleaned.replace(/\n{2,}/g, '\n'); //개행 제거 .. 전처리 부분
  cleaned=cleaned.replace(/\s{2,}/g, ' ');  //공백 하나로
  const adPatterns=[  //정규표현식(특정 패턴 검출출)..추가 필요
      /지금 구매 시.*/g,
      /이벤트.*\n?/g,
      /쿠폰 다운로드.*\n/g
  ];
  const adKeyWords=['최대 할인', '쿠폰', '초특가']; //특정 단어 검출..추가 필요요
  function removeAds(text){  //광고 제거 함수
      let result=text;
      adPatterns.forEach(p=>result=result.replace(p, ''));
      result=result.split('\n')
          .filter(line=>!adKeyWords.some(kw=>line.includes(kw)))
          .join('\n');
      return result;
  }
  cleaned=removeAds(cleaned); //광고 제거
  function chunkText(text, chunkSize=1000){  //chunk 분리 함수
      const chunks=[];
      for(let i=0;i<text.length;i+=chunkSize){
          chunks.push(text.slice(i, i+chunkSize));
      }
      return chunks;
  }      
  cleaned=chunkText(cleaned); //chunk로 분리
  return cleaned;
}

  fetch("http://localhost:5000/summarize", {  //localhost 일단 test용, 5000, summarize 추후 변경 가능
      method: "POST",  //전달 방법
      headers:{
          "Content-Type" : "application/json" //메타데이터
      },
      body: JSON.stringify({chunks: cleaned})  //json 형식으로 묶어서 fetch로 전송
  })
  .then(response=>response.json())  // 응답이 온 것을 다시 json 형식으로

  .then(data => {  //json 형식을 받아서.. 
let result = "";

try {
  const parsed = JSON.parse(data.summary);  //json 형태인지 확인 

  if (Array.isArray(parsed)) {  //배열인지 확인 
    result = parsed.map((item, index) => {  //map 에서 접근하여 아래 내용을 result에 저장
      return `[${index + 1}] ${item.name || '이름 없음'}  
가격: ${item.price || '없음'}
설명: ${item.description || '없음'}
이미지: ${item.image_url || '없음'}
링크: ${item.product_url || '없음'}\n`;
    }).join('\n');
  } else {
    result = JSON.stringify(parsed, null, 2); //배열이 아니면... 즉 하나의 상품이면 이와 같이 
  }

} catch (e) {  // json 형태가아니면면
  result = data
    .replace(/\n{2,}/g, '\n')
    .replace(/\s{2,}/g, ' ')
    .trim();
}

console.log("정돈된 결과:\n", result); //결과 출력

});

  /*.then(data=>{
      console.log("요약 결과:", data.summary); //요약 결과 출력
  });*/
  //cleaned.join('\n'); //다시 합치기  .. test 용
  //return cleaned; //return .. test 용v */
