from flask import Blueprint, render_template, current_app, jsonify
import os

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/api/templates')
def get_templates():
    classic_dir = 'classic'
    modern_dir = 'modern'
    
    templates = []
    
    if os.path.exists(classic_dir):
        for f in os.listdir(classic_dir):
            if f.endswith('.html'):
                templates.append({
                    "id": f,
                    "name": f.replace('.html', '').replace('-', ' ').title(),
                    "category": "classic",
                    "style": "Academic Serif",
                    "preview_url": f"/template_raw/classic/{f}"
                })
                
    if os.path.exists(modern_dir):
        for f in os.listdir(modern_dir):
            if f.endswith('.html'):
                templates.append({
                    "id": f,
                    "name": f.replace('.html', '').replace('_', ' ').replace('-', ' ').title(),
                    "category": "modern",
                    "style": "Contemporary Sans",
                    "preview_url": f"/template_raw/modern/{f}"
                })
                
    return jsonify(templates)

@main_bp.route('/templates')
def templates_gallery():
    # List templates from classic/ and modern/
    classic_templates = [f for f in os.listdir('classic') if f.endswith('.html')]
    modern_templates = [f for f in os.listdir('modern') if f.endswith('.html')]
    
    return render_template('gallery.html', 
                           classic=classic_templates, 
                           modern=modern_templates)

@main_bp.route('/template_raw/<category>/<name>')
def template_raw(category, name):
    if category not in ['classic', 'modern']:
        return "Invalid category", 400
    
    # Security check: prevent directory traversal
    name = os.path.basename(name)
    path = os.path.join(category, name)
    
    if not os.path.exists(path):
        return "Template not found", 404
        
    with open(path, 'r') as f:
        return f.read()
