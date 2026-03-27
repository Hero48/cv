# Design System Document

## 1. Overview & Creative North Star

### Creative North Star: "The Academic Rebel"
This design system moves away from the sterile, rigid structures often found in educational platforms. Instead, it embraces **Organic Brutalism**—a style that combines the raw honesty of Neo-Brutalist architecture with a warm, energetic, and growth-oriented spirit specifically tailored for young Ghanaian educators.

The system is built on "Intentional Impact." We break the "template" look by utilizing heavy black strokes, high-contrast shadows, and asymmetrical layouts that feel like a high-end editorial magazine rather than a standard SaaS dashboard. It communicates authority through bold typography and accessibility through a playful, vibrant color palette. Every element should feel physical, tactile, and grounded.

---

## 2. Colors

The palette is a sophisticated blend of grounded earthy tones and high-energy accents.

*   **Primary (Warm Gold):** `#715800` (Dim) / `#f8cd50` (Container). This is our signature "Ghanaian Gold." It represents excellence and prestige. Use `primary_container` for hero elements and main CTAs.
*   **Secondary (Mint Green):** `#00675c`. Represents growth and fresh starts. Use for success states and career advancement modules.
*   **Tertiary (Lavender/Pink):** `#734a90` / `#dcacfb`. These soft accents provide a youthful, modern edge that balances the heavy black borders.
*   **Neutral (Surface):** `#f6f6f6`. Our base is a warm off-white, providing a softer reading experience than pure white.

### The "No-Line" Rule for Layout
While components use heavy borders, **never use 1px solid grey lines** to section off the page. Transitions between major sections should be defined by shifts in background color (e.g., moving from `surface` to `surface_container_low`).

### Surface Hierarchy & Nesting
Treat the UI as a series of stacked, physical cards.
*   **Base:** `surface` (#f6f6f6)
*   **Sub-sections:** `surface_container` (#e7e8e8)
*   **Nested Elements:** `surface_container_highest` (#dbdddd)
This nesting creates depth through tonal shifts rather than relying on standard dividers.

### Signature Textures & Gradients
To elevate the look beyond "flat" Neo-Brutalism, use subtle linear gradients on large surfaces (e.g., `primary` to `primary_container`) to simulate a slight glow. This adds "soul" and professional polish to headers and large action cards.

---

## 3. Typography

The typography strategy relies on a "High-Low" contrast: a sophisticated Serif paired with a tech-forward Sans-Serif.

*   **Display & Headlines (Newsreader):** Use this high-contrast serif for all `display-lg` through `headline-sm`. It evokes the feeling of a prestigious academic journal but, when rendered at large scales with bold weights, feels radical and modern.
*   **Titles & Body (Space Grotesk):** Use this geometric sans-serif for all functional text. Its wide apertures and quirky character terminals complement the Neo-Brutalist aesthetic perfectly.

**Hierarchy Intent:**
Headlines should be unapologetically large (`display-lg`: 3.5rem) to command attention. Body text (`body-lg`: 1rem) must remain highly legible with generous line-height (1.6) to ensure the platform feels "accessible" rather than "dense."

---

## 4. Elevation & Depth

In this system, elevation is not a "suggestion"—it is a structural statement.

### The Brutalist Shadow
When an element needs to "pop," do not use soft, blurry shadows. Use a **Hard Offset Shadow**:
*   **X/Y Offset:** 4px (Small) to 8px (Large).
*   **Blur:** 0px.
*   **Color:** `on_background` (#2d2f2f) at 100% opacity.
This creates a "sticker" effect that feels tactile and bold.

### Glassmorphism & Depth
For floating navigation bars or overlays, use **Glassmorphism**. Apply a semi-transparent `surface` color with a `backdrop-blur` of 12px-20px. This softens the aggressive borders of the content underneath, making the UI feel layered and premium.

### The "Ghost Border" Fallback
Where a container needs definition without the weight of a 4px black border, use a **Ghost Border**: `outline_variant` at 20% opacity. **Never use 100% opaque thin grey lines.**

---

## 5. Components

### Buttons
*   **Primary:** `primary_container` background, 3px solid `on_background` border. Hard shadow (4px).
*   **Secondary:** `secondary_container` background, 2px solid `on_background` border.
*   **States:** On hover, the button should "press down" (Shadow offset becomes 0px, and the button translates 4px down/right).

### Cards
*   **Style:** No dividers. Use `spacing.6` (2rem) of internal padding.
*   **Border:** Always 2px to 4px black.
*   **Separation:** Use background color shifts (`surface_container_low`) to distinguish between card types rather than adding more borders.

### Input Fields
*   **Style:** Rectangular, `roundedness.md`.
*   **Border:** 2px solid `on_background`.
*   **Focus State:** Background shifts to `primary_fixed_dim` with a hard 4px shadow.

### Chips & Tags
*   **Style:** Pill-shaped (`roundedness.full`).
*   **Colors:** Use `tertiary_container` or `secondary_fixed` to make these feel like vibrant "stickers" on the page.

---

## 6. Do's and Don'ts

### Do:
*   **Do** embrace asymmetry. Allow images or decorative elements to "break" the container borders.
*   **Do** use the Spacing Scale strictly. Generous white space (e.g., `spacing.12`) is required to balance the heavy black strokes.
*   **Do** mix the fonts. A Serif headline over Sans-Serif body text is the "signature" of this system.

### Don't:
*   **Don't** use 1px grey borders. They look "cheap" and "default."
*   **Don't** use soft, blurry drop shadows unless it's a specific "Glass" overlay.
*   **Don't** crowd the interface. Neo-Brutalism requires "breathing room" to keep it from feeling overwhelming.
*   **Don't** use pure black (#000000) for borders; use `on_background` (#2d2f2f) to keep the contrast high but the tone sophisticated.