from flask import Blueprint, request, jsonify
from ..services.review_summary import summarize_review_info

review_bp = Blueprint("review", __name__)

@review_bp.route("/review-summary", methods=["POST"])
def review_summary():
    review_data = request.get_json()
    result = summarize_review_info(review_data)
    return jsonify(result)