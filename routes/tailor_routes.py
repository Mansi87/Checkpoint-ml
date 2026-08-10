from flask import Blueprint, request, jsonify
from services.tailor_service import tailor_resume

tailor_bp = Blueprint('tailor', __name__)


@tailor_bp.route('/tailor-resume', methods=['POST'])
def tailor():
    data = request.get_json()

    resume_context = data.get('resume_context')
    jd_text = data.get('jd_text', '')
    missing_keywords = data.get('missing_keywords', [])
    user_status = data.get('user_status', 'working')

    if not resume_context or not jd_text:
        return jsonify({"error": "resume_context and jd_text are required"}), 400

    try:
        result = tailor_resume(resume_context, jd_text, missing_keywords, user_status)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500