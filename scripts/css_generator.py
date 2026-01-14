#!/usr/bin/env python3
"""
CSS Generator Module - Handles all CSS generation for the website builder.

This module extracts CSS generation logic from build_website.py for better maintainability.
Includes:
- Base styles and CSS custom properties
- Layout variants (newspaper, magazine, dashboard, minimal, bold, mosaic)
- Hero styles (12 variants with animations)
- Card styles and hover effects
- Accessibility features (focus states, reduced motion)
- CSS minification
"""

import re
from typing import Dict, Optional


def minify_css(css: str) -> str:
    """
    Minify CSS by removing comments, whitespace, and unnecessary characters.

    Args:
        css: Raw CSS string

    Returns:
        Minified CSS string (typically 30-50% smaller)
    """
    # Remove CSS comments
    css = re.sub(r'/\*[\s\S]*?\*/', '', css)

    # Remove newlines and extra whitespace
    css = re.sub(r'\s+', ' ', css)

    # Remove whitespace around special characters
    css = re.sub(r'\s*([{};:,>+~])\s*', r'\1', css)

    # Remove trailing semicolons before closing braces
    css = re.sub(r';}', '}', css)

    # Remove leading/trailing whitespace
    css = css.strip()

    return css


def get_base_css(design: Dict, hero_bg: str) -> str:
    """Generate base CSS variables and reset styles."""
    d = design

    # Extract design properties with fallbacks
    card_radius = d.get('card_radius', '1rem')
    card_padding = d.get('card_padding', '1.5rem')
    spacing = d.get('spacing', 'comfortable')
    animation_level = d.get('animation_level', 'subtle')
    accent = d.get('color_accent', '#6366f1')
    accent_secondary = d.get('color_accent_secondary', '#8b5cf6')

    # Dark mode defaults
    dark_bg = '#0a0a0a'
    dark_text = '#ffffff'
    dark_muted = '#a1a1aa'
    dark_card_bg = '#18181b'
    dark_border = '#27272a'

    # Spacing map
    spacing_map = {'compact': '2rem', 'comfortable': '3rem', 'spacious': '4rem'}
    section_gap = spacing_map.get(spacing, '3rem')

    # Animation duration map
    anim_map = {'none': '0s', 'subtle': '0.3s', 'moderate': '0.4s', 'playful': '0.5s', 'energetic': '0.25s'}
    anim_duration = anim_map.get(animation_level, '0.3s')

    return f"""
:root {{
    --color-bg: {dark_bg};
    --color-text: {dark_text};
    --color-accent: {accent};
    --color-accent-secondary: {accent_secondary};
    --color-muted: {dark_muted};
    --color-card-bg: {dark_card_bg};
    --color-border: {dark_border};
    --font-primary: '{d.get('font_primary', 'Space Grotesk')}', system-ui, sans-serif;
    --font-secondary: '{d.get('font_secondary', 'Inter')}', system-ui, sans-serif;
    --radius-sm: calc({card_radius} * 0.5);
    --radius: {card_radius};
    --radius-lg: calc({card_radius} * 1.5);
    --radius-xl: calc({card_radius} * 2);
    --card-padding: {card_padding};
    --section-gap: {section_gap};
    --transition: {anim_duration} cubic-bezier(0.4, 0, 0.2, 1);
    --transition-fast: calc({anim_duration} * 0.5) cubic-bezier(0.4, 0, 0.2, 1);
    --transition-slow: calc({anim_duration} * 1.5) cubic-bezier(0.4, 0, 0.2, 1);
    --max-width: {d.get('max_width', '1400px')};
    --hero-bg: {hero_bg};
}}

*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
html {{ scroll-behavior: smooth; font-size: 16px; }}
body {{
    font-family: var(--font-secondary);
    line-height: 1.6;
    color: var(--color-text);
    background: var(--color-bg);
    min-height: 100vh;
    overflow-x: hidden;
    transition: background-color 0.3s ease, color 0.3s ease;
}}
a {{ color: inherit; text-decoration: none; }}
img {{ max-width: 100%; height: auto; }}
"""


def get_typography_css() -> str:
    """Generate typography styles."""
    return """
.headline-xl {{
    font-family: var(--font-primary);
    font-size: clamp(2.5rem, 8vw, 5rem);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.02em;
}}
.headline-lg {{
    font-family: var(--font-primary);
    font-size: clamp(1.75rem, 4vw, 3rem);
    font-weight: 700;
    line-height: 1.1;
}}
.headline-md {{
    font-family: var(--font-primary);
    font-size: clamp(1.25rem, 2.5vw, 1.75rem);
    font-weight: 600;
    line-height: 1.2;
}}
.text-muted {{ color: var(--color-muted); }}
.text-transform-uppercase .headline-xl,
.text-transform-uppercase .headline-lg,
.text-transform-uppercase .headline-md,
.text-transform-uppercase .section-title,
.text-transform-uppercase .story-title {{
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}
.text-transform-capitalize .headline-xl,
.text-transform-capitalize .headline-lg,
.text-transform-capitalize .headline-md,
.text-transform-capitalize .section-title,
.text-transform-capitalize .story-title {{
    text-transform: capitalize;
}}
"""


def get_accessibility_css() -> str:
    """Generate accessibility-focused CSS including skip link and focus states."""
    return """
/* Skip link for keyboard navigation */
.skip-link {
    position: absolute;
    top: -100%;
    left: 0;
    background: var(--color-accent);
    color: white;
    padding: 0.75rem 1.5rem;
    z-index: 1000;
    font-weight: 600;
    border-radius: 0 0 var(--radius-sm) 0;
    transition: top 0.2s ease;
}
.skip-link:focus {
    top: 0;
    outline: 3px solid var(--color-accent);
    outline-offset: 2px;
}

/* Focus states for all interactive elements */
a:focus-visible,
button:focus-visible,
.story-card:focus-visible,
.compact-card:focus-visible,
input:focus-visible,
select:focus-visible,
textarea:focus-visible,
[tabindex]:focus-visible {
    outline: 3px solid var(--color-accent);
    outline-offset: 2px;
    border-radius: var(--radius-sm);
}

/* Minimum touch target size (44x44px) */
.nav-links a,
.theme-toggle,
.nav-github,
.story-card,
.compact-card,
button {
    min-height: 44px;
    min-width: 44px;
}

/* Reduced motion preference */
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
    }
    .animate-fade-up, .animate-fade-left, .animate-fade-right,
    .animate-scale-in, .animate-slide-up {
        animation: none !important;
        opacity: 1 !important;
        transform: none !important;
    }
}
"""


def get_animation_css() -> str:
    """Generate scroll-triggered animation keyframes and classes."""
    return """
/* Scroll-triggered animation keyframes */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes fadeInLeft {
    from { opacity: 0; transform: translateX(-30px); }
    to { opacity: 1; transform: translateX(0); }
}
@keyframes fadeInRight {
    from { opacity: 0; transform: translateX(30px); }
    to { opacity: 1; transform: translateX(0); }
}
@keyframes scaleIn {
    from { opacity: 0; transform: scale(0.9); }
    to { opacity: 1; transform: scale(1); }
}
@keyframes slideUp {
    from { opacity: 0; transform: translateY(50px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}
@keyframes bounce {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.2); }
}

/* Animation classes */
.animate-fade-up { animation: fadeInUp 0.6s ease-out forwards; opacity: 0; }
.animate-fade-left { animation: fadeInLeft 0.6s ease-out forwards; opacity: 0; }
.animate-fade-right { animation: fadeInRight 0.6s ease-out forwards; opacity: 0; }
.animate-scale-in { animation: scaleIn 0.5s ease-out forwards; opacity: 0; }
.animate-slide-up { animation: slideUp 0.5s cubic-bezier(0.4, 0, 0.2, 1) forwards; opacity: 0; }

/* Stagger delays */
.stagger-1 { animation-delay: 0.05s; }
.stagger-2 { animation-delay: 0.1s; }
.stagger-3 { animation-delay: 0.15s; }
.stagger-4 { animation-delay: 0.2s; }
.stagger-5 { animation-delay: 0.25s; }
.stagger-6 { animation-delay: 0.3s; }
.stagger-7 { animation-delay: 0.35s; }
.stagger-8 { animation-delay: 0.4s; }

/* Animation level variants */
.animation-none *, .animation-none *::before, .animation-none *::after {
    animation: none !important;
    transition: none !important;
}
.animation-playful .story-card {
    transition-timing-function: cubic-bezier(0.68, -0.55, 0.265, 1.55);
}
.animation-playful .word-cloud-item:hover {
    animation: bounce 0.5s ease;
}
"""


def get_image_treatment_css() -> str:
    """Generate CSS for image treatment filters."""
    return """
/* Image treatments */
.image-treatment-grayscale .story-image,
.image-treatment-grayscale .card-image { filter: grayscale(100%); }
.image-treatment-sepia .story-image,
.image-treatment-sepia .card-image { filter: sepia(30%); }
.image-treatment-saturate .story-image,
.image-treatment-saturate .card-image { filter: saturate(1.3); }
.image-treatment-contrast .story-image,
.image-treatment-contrast .card-image { filter: contrast(1.1); }
.image-treatment-vignette .story-image,
.image-treatment-vignette .card-image { box-shadow: inset 0 0 100px rgba(0,0,0,0.5); }
.image-treatment-duotone_warm .story-image,
.image-treatment-duotone_warm .card-image { filter: sepia(20%) saturate(1.2) hue-rotate(-10deg); }
.image-treatment-duotone_cool .story-image,
.image-treatment-duotone_cool .card-image { filter: saturate(0.8) hue-rotate(20deg); }
"""


def get_card_aspect_ratio_css() -> str:
    """Generate CSS for card aspect ratio variations."""
    return """
/* Card aspect ratios */
.aspect-landscape .story-card .story-image,
.aspect-landscape .card-image { aspect-ratio: 16/9; object-fit: cover; }
.aspect-portrait .story-card .story-image,
.aspect-portrait .card-image { aspect-ratio: 3/4; object-fit: cover; }
.aspect-square .story-card .story-image,
.aspect-square .card-image { aspect-ratio: 1/1; object-fit: cover; }
.aspect-wide .story-card .story-image,
.aspect-wide .card-image { aspect-ratio: 21/9; object-fit: cover; }
.aspect-classic .story-card .story-image,
.aspect-classic .card-image { aspect-ratio: 4/3; object-fit: cover; }
"""


def get_section_divider_css() -> str:
    """Generate CSS for section dividers."""
    return """
/* Section dividers */
.section-divider { margin: 2rem 0; }
.section-divider-line { border-top: 1px solid var(--color-border); }
.section-divider-thick_line { border-top: 3px solid var(--color-accent); }
.section-divider-gradient_line {
    background: linear-gradient(90deg, transparent, var(--color-accent), transparent);
    height: 2px;
}
.section-divider-dots {
    background: radial-gradient(circle, var(--color-accent) 2px, transparent 2px);
    background-size: 20px 20px;
    height: 10px;
}
.section-divider-fade {
    background: linear-gradient(180deg, var(--color-bg), var(--color-card-bg));
    height: 40px;
}
"""


def get_lazy_loading_css() -> str:
    """Generate CSS for lazy loading placeholder states."""
    return """
/* Lazy loading placeholders */
.lazy-placeholder {
    background: linear-gradient(90deg, var(--color-card-bg) 25%, var(--color-border) 50%, var(--color-card-bg) 75%);
    background-size: 200% 100%;
    animation: shimmer 1.5s infinite;
    min-height: 200px;
    border-radius: var(--radius);
}
@keyframes shimmer {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}
.lazy-loaded {
    animation: fadeIn 0.3s ease-out;
}
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}
"""


def generate_complete_css(design: Dict, hero_bg: str, enable_minification: bool = True) -> str:
    """
    Generate the complete CSS stylesheet for the website.

    Args:
        design: Design specification dictionary
        hero_bg: CSS background value for hero section
        enable_minification: Whether to minify the output (default True)

    Returns:
        Complete CSS string (minified if enabled)
    """
    css_parts = [
        get_base_css(design, hero_bg),
        get_typography_css(),
        get_accessibility_css(),
        get_animation_css(),
        get_image_treatment_css(),
        get_card_aspect_ratio_css(),
        get_section_divider_css(),
        get_lazy_loading_css(),
    ]

    complete_css = '\n'.join(css_parts)

    if enable_minification:
        return minify_css(complete_css)

    return complete_css
