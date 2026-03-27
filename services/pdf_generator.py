from playwright.sync_api import sync_playwright
import os

def generate_pdf(url, output_path):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        
        # Give a bit more time for any late rendering
        page.wait_for_timeout(1000)
        
        page.pdf(path=output_path, format="A4", print_background=True)
        browser.close()
