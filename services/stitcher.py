from bs4 import BeautifulSoup
import os

class CVStitcher:
    def __init__(self, template_path):
        with open(template_path, 'r') as f:
            self.soup = BeautifulSoup(f.read(), 'html.parser')
            
    def stitch(self, data):
        # 1. Replace Name (heuristic: find H1)
        name_tag = self.soup.find('h1')
        if name_tag:
            name_tag.string = data.get('full_name', '')
            
        # 2. Replace Summary (heuristic: find first P in a section with 'Summary' or 'About')
        # This is very template-dependent. For the MVP, we'll look for specific patterns.
        
        # 3. Handle Contact Info
        # Look for text containing '@' or '+'
        for span in self.soup.find_all(['span', 'p', 'div']):
            if '@' in span.text and data.get('email'):
                span.string = data['email']
            if '+' in span.text and data.get('phone'):
                span.string = data['phone']
                
        # 4. Handle Sections (Experience, Education)
        # This is the hardest part. For now, we'll return the HTML as is 
        # but with the name/contact replaced.
        
        return str(self.soup)

def render_preview(template_rel_path, data, is_paid=False):
    # For now, we'll use a very simple replacement logic
    template_path = os.path.join(os.getcwd(), template_rel_path)
    stitcher = CVStitcher(template_path)
    html = stitcher.stitch(data)
    
    if not is_paid:
        # Inject Watermark CSS and Overlay
        watermark_html = """
        <style>
            .watermark {
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%) rotate(-45deg);
                font-size: 100px;
                color: rgba(200, 0, 0, 0.2);
                z-index: 9999;
                pointer-events: none;
                white-space: nowrap;
                font-family: sans-serif;
                font-weight: bold;
                text-transform: uppercase;
            }
        </style>
        <div class="watermark">PREVIEW ONLY - UPGRADE TO DOWNLOAD</div>
        """
        html = html.replace('</body>', watermark_html + '</body>')
        
    return html
