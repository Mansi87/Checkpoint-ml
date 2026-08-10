from flask import Blueprint, request, jsonify
from services.jd_service import analyze_jd

jd_bp = Blueprint('jd', __name__)


@jd_bp.route('/analyze-jd', methods=['POST'])
def analyze():
    data = request.get_json()

    resume_text = data.get('resume_text', '')
    jd_text = data.get('jd_text', '')

    if not resume_text or not jd_text:
        return jsonify({"error": "resume_text and jd_text are required"}), 400

    result = analyze_jd(resume_text, jd_text)
    return jsonify(result), 200