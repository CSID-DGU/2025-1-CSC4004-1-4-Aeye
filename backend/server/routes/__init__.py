from flask import Blueprint

# 각각의 기능별 라우터 import
from .product_route import summary_bp
from .review_route import review_bp
from .tts_route import tts_bp

# Blueprint들을 모아 export
all_blueprints = [summary_bp, review_bp, tts_bp]