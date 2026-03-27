from flask import Blueprint, render_template, request, session, jsonify, send_file, url_for
import os
import google.generativeai as genai
import json
import tempfile
from services.stitcher import render_preview
from services.pdf_generator import generate_pdf

ai_bp = Blueprint('ai', __name__)

# Configure Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Use a model that exists in 2026
MODEL_NAME = 'gemini-3-flash-preview'

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
    
    model = genai.GenerativeModel(MODEL_NAME)
    
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
    
    # Format history for Gemini
    messages = [{"role": "user", "parts": [system_instruction]}]
    for msg in history:
        messages.append({"role": msg['role'], "parts": [msg['content']]})
    
    messages.append({"role": "user", "parts": [user_msg]})
    
    try:
        response = model.generate_content(messages)
        ai_content = response.text
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    history.append({"role": "user", "content": user_msg})
    history.append({"role": "model", "content": ai_content})
    session['chat_history'] = history
    
    return jsonify({"response": ai_content, "is_ready": "[READY]" in ai_content})

@ai_bp.route('/refine')
def refine_data():
    history = session.get('chat_history', [])
    if not history:
        return "No chat history found", 400
        
    # Extract structured data using Gemini
    model = genai.GenerativeModel(MODEL_NAME, generation_config={"response_mime_type": "application/json"})
    
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
        response = model.generate_content(prompt)
        extracted_data = json.loads(response.text)
        session['extracted_data'] = extracted_data
        
        # CLEAR CHAT HISTORY TO SAVE SESSION SPACE (Browser 4KB limit)
        # We've already extracted what we need.
        session.pop('chat_history', None)
        # Keep selected_template, it's small but vital
    except Exception as e:
        return f"Error extracting data: {str(e)}", 500
        
    return render_template('refine.html', data=extracted_data)

@ai_bp.route('/preview', methods=['POST'])
def preview_cv():
    # Update extracted_data with user changes
    data = session.get('extracted_data', {})
    if not data:
        # If session was lost, try to recover at least basic structure
        data = {'contact': {}}
    
    data['full_name'] = request.form.get('full_name')
    
    if 'contact' not in data:
        data['contact'] = {}
    data['contact']['location'] = request.form.get('location', '')
    data['contact']['email'] = request.form.get('email', '')
    data['contact']['phone'] = request.form.get('phone', '')
    
    data['professional_summary'] = request.form.get('summary', '')
    session['extracted_data'] = data
    
    # Ensure selected_template is still there
    if not session.get('selected_template'):
        return "Session expired or lost. Please go back to gallery.", 400
    
    return render_template('preview.html')

@ai_bp.route('/render_cv')
def render_cv_html():
    # This route is used by the iframe in preview.html and by Playwright
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
        # Cleanup temp HTML file
        if os.path.exists(temp_html_path):
            os.remove(temp_html_path)
