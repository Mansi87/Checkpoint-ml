from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from flask_cors import CORS
from routes.jd_routes import jd_bp
from routes.tailor_routes import tailor_bp
from routes.parse_routes import parse_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(jd_bp, url_prefix='/api')
app.register_blueprint(tailor_bp, url_prefix='/api')
app.register_blueprint(parse_bp, url_prefix='/api')

@app.route('/health', methods=['GET'])
def health():
    return {"status": "ok"}, 200

if __name__ == '__main__':
    app.run(port=5001, debug=True)
