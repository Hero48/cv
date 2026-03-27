from bs4 import BeautifulSoup
import os

class CVStitcher:
    def __init__(self, template_path):
        with open(template_path, 'r') as f:
            self.soup = BeautifulSoup(f.read(), 'html.parser')
            
    def stitch(self, data):
        # 1. Name & Professional Summary
        name_tag = self.soup.find('h1')
        if name_tag:
            name_tag.string = data.get('full_name', '')
            
        summary_tag = self.soup.find(class_='summary-text') or self.soup.find('p', class_='summary')
        if summary_tag:
            summary_tag.string = data.get('professional_summary', '')
            
        # 2. Contact Info
        for span in self.soup.find_all(['span', 'p', 'div', 'a']):
            text = span.get_text()
            if '@' in text and data.get('contact', {}).get('email'):
                span.string = data['contact']['email']
            elif ('+' in text or any(c.isdigit() for c in text)) and data.get('contact', {}).get('phone'):
                # Heuristic: if it looks like a phone placeholder
                if 'phone' in span.get('class', []) or 'contact' in span.get('class', []):
                    span.string = data['contact']['phone']

        # 3. Dynamic Sections (Experience)
        # Find the Experience section
        exp_section = None
        for section in self.soup.find_all(class_='section'):
            label = section.find(class_='section-label')
            if label and 'experience' in label.get_text().lower():
                exp_section = section
                break
        
        if exp_section and data.get('experience'):
            # Find the template entry to clone
            template_entry = exp_section.find(class_='entry')
            if template_entry:
                # Clear existing entries
                for entry in exp_section.find_all(class_='entry'):
                    entry.decompose()
                
                # Add new entries from data
                for item in data['experience']:
                    new_entry = self.soup.new_tag("div", attrs={"class": "entry"})
                    
                    header = self.soup.new_tag("div", attrs={"class": "entry-header"})
                    title = self.soup.new_tag("div", attrs={"class": "entry-title"})
                    title.string = item.get('role', '')
                    date = self.soup.new_tag("div", attrs={"class": "entry-date"})
                    date.string = item.get('dates', '')
                    header.append(title)
                    header.append(date)
                    
                    company = self.soup.new_tag("div", attrs={"class": "entry-company"})
                    company.string = item.get('company', '')
                    
                    desc_list = self.soup.new_tag("ul", attrs={"class": "entry-desc"})
                    for achievement in item.get('achievements', []):
                        li = self.soup.new_tag("li")
                        li.string = achievement
                        desc_list.append(li)
                    
                    new_entry.append(header)
                    new_entry.append(company)
                    new_entry.append(desc_list)
                    exp_section.append(new_entry)

        # 4. Dynamic Sections (Education)
        edu_section = None
        for section in self.soup.find_all(class_='section'):
            label = section.find(class_='section-label')
            if label and 'education' in label.get_text().lower():
                edu_section = section
                break
        
        if edu_section and data.get('education'):
            template_entry = edu_section.find(class_='entry')
            if template_entry:
                for entry in edu_section.find_all(class_='entry'):
                    entry.decompose()
                
                for item in data['education']:
                    new_entry = self.soup.new_tag("div", attrs={"class": "entry"})
                    header = self.soup.new_tag("div", attrs={"class": "entry-header"})
                    title = self.soup.new_tag("div", attrs={"class": "entry-title"})
                    title.string = item.get('degree', '')
                    date = self.soup.new_tag("div", attrs={"class": "entry-date"})
                    date.string = item.get('year', '')
                    header.append(title)
                    header.append(date)
                    
                    inst = self.soup.new_tag("div", attrs={"class": "entry-company"})
                    inst.string = item.get('institution', '')
                    
                    new_entry.append(header)
                    new_entry.append(inst)
                    edu_section.append(new_entry)

        # 5. Skills
        skills_section = None
        for section in self.soup.find_all(class_='section'):
            label = section.find(class_='section-label')
            if label and 'skills' in label.get_text().lower():
                skills_section = section
                break
        
        if skills_section and data.get('skills'):
            # Many templates use a wrapper for skills
            wrapper = skills_section.find(class_='skills-wrapper') or skills_section
            # Try to find individual skill tags to replace
            skill_tags = wrapper.find_all(class_='skill-tag')
            if skill_tags:
                for tag in skill_tags: tag.decompose()
                for s in data['skills']:
                    new_tag = self.soup.new_tag("span", attrs={"class": "skill-tag"})
                    new_tag.string = s
                    wrapper.append(new_tag)
        
        return str(self.soup)

def render_preview(template_rel_path, data, is_paid=False):
    template_path = os.path.join(os.getcwd(), template_rel_path)
    stitcher = CVStitcher(template_path)
    html = stitcher.stitch(data)
    
    if not is_paid:
        watermark_html = """
        <style>
            .watermark {
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%) rotate(-45deg);
                font-size: 80px;
                color: rgba(0, 0, 0, 0.1);
                z-index: 9999;
                pointer-events: none;
                white-space: nowrap;
                font-family: sans-serif;
                font-weight: bold;
                text-transform: uppercase;
                border: 10px solid rgba(0,0,0,0.1);
                padding: 20px;
            }
        </style>
        <div class="watermark">PREVIEW ONLY - UPGRADE TO DOWNLOAD</div>
        """
        html = html.replace('</body>', watermark_html + '</body>')
        
    return html
