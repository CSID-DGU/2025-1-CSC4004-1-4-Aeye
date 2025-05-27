from flask import Blueprint, request, jsonify
from services.product_summary import summarize_basic_info, summarize_detail_info

summary_bp = Blueprint("summary", __name__)

@summary_bp.route("/summary/basic", methods=["POST"])
def summarize_basic():
    html_text = request.json.get("text", "")
    result = summarize_basic_info(html_text)
    return jsonify(result)

@summary_bp.route("/summary/detail", methods=["POST"])
def summarize_detail_with_images():
    image_paths = request.json.get("imagePaths", [])
    result = summarize_detail_info_from_images(image_paths)
    return jsonify(result)