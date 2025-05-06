// utils.js: 공통 함수 모음
export function formatPrice(priceString) {
  return parseInt(priceString.replace(/[^\d]/g, ""), 10);
}
