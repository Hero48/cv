from flask import Blueprint, render_template, request, session, jsonify, send_file, url_for
import os
from google import genai
import json
import tempfile
from services.stitcher import render_preview
from services.pdf_generator import generate_pdf

ai_bp = Blueprint('ai', __name__)

# Configure Gemini Client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
MODEL_NAME = 'gemini-2.0-flash' # Current 2026 standard

@ai_bp.route('/chat')
def chat_interview():
    template = request.args.get('template')
    category = request.args.get('category')
    
    if not template or not category:
        return "Missing template or category", 400
        
    session['selected_template'] = f"{category}/{template}"
    session['chat_history'] = []
    
    return render_template('chat.html', template=template)

@ai_bp.route('/api/chat', methods=['POST'])
def chat_api():
    user_msg = request.json.get('message')
    history = session.get('chat_history', [])
    
    # System Instruction for "The Academic Rebel"
    system_instruction = """
    You are 'The Academic Rebel', a mentor for Ghanaian educators. 
    Your goal is to help them build a high-impact CV.
    Be encouraging, professional, but bold and energetic.
    Ask progressive questions one at a time to gather:
    1. Full Name and Contact Info.
    2. Professional Summary.
    3. Work Experience (Company, Role, Dates, Achievements).
    4. Education (Institution, Degree, Year).
    5. Skills and Certifications.
    
    Keep responses concise and use Ghanaian educational context (e.g., mentioning GES, BECE, WASSCE where appropriate).
    Once you have enough info, say [READY] and provide a summary.
    """
    
    # Format history for the new SDK
    # We'll just use a simple prompt for now to keep it straightforward
    full_prompt = f"{system_instruction}\n\n"
    for msg in history:
        role_label = "Mentor" if msg['role'] == 'model' else "Educator"
        full_prompt += f"{role_label}: {msg['content']}\n"
    full_prompt += f"Educator: {user_msg}\nMentor:"

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=full_prompt
        )
        ai_content = response.text
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    history.append({"role": "user", "content": user_msg})
    history.append({"role": "model", "content": ai_content})
    session['chat_history'] = history
    
    return jsonify({"response": ai_content, "is_ready": "[READY]" in ai_content})

@ai_bp.route('/api/extracted_data')
def get_extracted_data():
    data = session.get('extracted_data')
    if not data:
        return jsonify({"error": "No data found"}), 404
    return jsonify(data)

@ai_bp.route('/api/refine', methods=['POST'])
def refine_data_api():
    history = session.get('chat_history', [])
    if not history:
        return jsonify({"error": "No chat history found"}), 400
        
    prompt = f"""
    Based on the following chat history between an educator and a mentor, extract the CV details into a structured JSON object.
    Required fields:
    - full_name
    - professional_summary
    - contact (email, phone, location)
    - experience (list of: company, role, dates, achievements[])
    - education (list of: institution, degree, year)
    - skills (list of strings)
    
    Chat History:
    {json.dumps(history)}
    """
    
    try:
        # Using the new SDK's JSON output capability
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config={
                'response_mime_type': 'application/json'
            }
        )
        extracted_data = json.loads(response.text)
        session['extracted_data'] = extracted_data
        session.pop('chat_history', None)
        return jsonify(extracted_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ai_bp.route('/preview', methods=['POST'])
def preview_cv():
    data = session.get('extracted_data', {})
    if not data:
        data = {'contact': {}}
    
    if request.is_json:
        new_data = request.json
        data.update(new_data)
    else:
        data['full_name'] = request.form.get('full_name')
        if 'contact' not in data:
            data['contact'] = {}
        data['contact']['location'] = request.form.get('location', '')
        data['contact']['email'] = request.form.get('email', '')
        data['contact']['phone'] = request.form.get('phone', '')
        data['professional_summary'] = request.form.get('summary', '')
    
    session['extracted_data'] = data
    
    if not session.get('selected_template'):
        return jsonify({"error": "Session expired or lost. Please go back to gallery."}), 400
    
    if request.is_json:
        return jsonify({"success": True})
    return render_template('preview.html')

@ai_bp.route('/render_cv')
def render_cv_html():
    data = session.get('extracted_data')
    template = session.get('selected_template')
    is_paid = request.args.get('is_paid', 'false').lower() == 'true'
    
    if not data or not template:
        return "No data found", 400
        
    html = render_preview(template, data, is_paid=is_paid)
    return html

@ai_bp.route('/download')
def download_pdf():
    data = session.get('extracted_data')
    template = session.get('selected_template')
    
    if not data or not template:
        return "No data found", 400
        
    html = render_preview(template, data, is_paid=True)
    
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as f:
        f.write(html.encode('utf-8'))
        temp_html_path = f.name
        
    output_pdf = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False).name
    
    try:
        generate_pdf(f"file://{temp_html_path}", output_pdf)
        return send_file(output_pdf, as_attachment=True, download_name=f"CV_{data.get('full_name', 'EduCV')}.pdf")
    finally:
        if os.path.exists(temp_html_path):
            os.remove(temp_html_path)
