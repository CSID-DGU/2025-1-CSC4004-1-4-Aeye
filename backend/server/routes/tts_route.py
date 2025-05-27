from flask import Blueprint, request, jsonify
from services.tts_generator import generate_tts_script

tts_bp = Blueprint("tts", __name__)

@tts_bp.route("/tts", methods=["POST"])
def tts_script():
    summary = request.json.get("summary", {})
    mode = request.json.get("mode", "basic")
    result = generate_tts_script(summary, mode)
    return jsonify({"script": result})
