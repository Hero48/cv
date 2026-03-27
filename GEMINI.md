# EduCV SaaS - Project Guidelines

## Project Overview
**EduCV** is transforming from a simple local tool into a full-fledged SaaS platform. The core value proposition remains the same: an AI-powered CV generator for educators. However, the architecture is pivoting to support user accounts, a template marketplace, and a conversational AI interface.

## Core Features & Requirements

### 1. Template Marketplace (Frontend)
- **Visual Gallery:** Users must be able to browse templates from the `classic/` and `modern/` directories.
- **Preview:** Each template needs a high-fidelity preview. Since these are raw HTML files, the frontend should render them (e.g., in iframes or by parsing the HTML) to show the user what they look like.
- **Selection:** Users select a template which becomes the target for their data.

### 2. Conversational AI Data Collection (Gemini Integration)
- **Chat Interface:** Instead of a static form, the user interacts with an AI agent (powered by Gemini).
- **Workflow:**
    1.  **Interview:** The AI asks progressive questions to gather CV details (Experience, Education, Skills, etc.).
    2.  **Refinement:** The AI suggests improvements (e.g., "This bullet point is weak, shall we say 'Led a team of 5' instead?").
    3.  **Generation:** Once confirmed, the structured data is merged with the selected HTML template.

### 3. Monetization & Security
- **Freemium Model:**
    - **Draft/Preview:** Users can generate and view their CV for free, but it **MUST** have a watermark overlay (e.g., "PREVIEW ONLY - UPGRADE TO DOWNLOAD").
    - **Download:** PDF download is locked behind a payment gate.
- **Payment Integration:** (Implementation details TBD, but architecture must support webhooks/callbacks to unlock files).

## Technical Architecture (Proposed)

- **Frontend:** Modern JavaScript Framework (React/Next.js or Vue/Nuxt.js recommended for state management of the chat and template gallery).
- **Backend:** Node.js/Express (continuing from previous iteration).
- **Database:** MongoDB or PostgreSQL (to store user sessions, chat history, and drafted CVs).
- **AI Engine:** Google Gemini API (for chat and JSON extraction).
- **PDF Generation:** Puppeteer or Playwright (for high-fidelity HTML-to-PDF conversion).

## Directory Structure
- `classic/`: Contains traditional, serif-heavy HTML templates.
- `modern/`: Contains contemporary, sans-serif, and experimental HTML templates.
- `stitch_educv_business_brief/`: Design assets and conceptual documents.

## Development Conventions
- **Templates:** Templates are standalone HTML files with inline CSS. They should be treated as "dumb" views that receive JSON data.
- **Watermarking:** Implement watermarking via a CSS overlay injected during the preview render, which is removed only when the "Paid" flag is true during PDF generation.
- **Chat Flow:** The chatbot should maintain context. Do not just ask for "Resume Text"; guide the user section by section.

## Next Steps
1.  Set up the backend to serve the template files as a JSON API (metadata + preview URL).
2.  Build the frontend gallery.
3.  Implement the Gemini chat loop.
