from flask import Blueprint, request, jsonify
from ..services.product_summary import summarize_basic_info, summarize_detail_info

summary_bp = Blueprint("summary", __name__)

@summary_bp.route("/summary/basic", methods=["POST"])
def summarize_basic():
    basic_data = request.get_json()
    result = summarize_basic_info(basic_data)
    return jsonify(result)

@summary_bp.route("/summary/detail", methods=["POST"])
def summarize_detail_with_images():
    detail_data = request.get_json()
    result = summarize_detail_info(detail_data)
    return jsonify(result)