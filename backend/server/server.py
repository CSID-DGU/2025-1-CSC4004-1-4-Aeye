from flask import Flask
from flask_cors import CORS
from .routes import all_blueprints

app = Flask(__name__)
CORS(app)

# 모든 라우터 등록
for bp in all_blueprints:
    app.register_blueprint(bp)

if __name__ == "__main__":
    app.run(port=5000)