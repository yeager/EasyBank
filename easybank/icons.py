"""Inline SVG pictogram icons for budget categories.

These are simple, clear pictograms designed for accessibility,
compatible with ARASAAC-style visual communication.
"""

# All icons are 64x64 SVG with thick strokes and clear shapes
# Colors follow a consistent, high-contrast palette

ICONS = {
    "food": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
      <circle cx="32" cy="32" r="30" fill="#FFF3E0" stroke="#E65100" stroke-width="3"/>
      <path d="M20 18v28M20 18c0-4 4-6 8-2v12h-8" fill="none" stroke="#E65100" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M38 18v10c0 4 2 6 4 6v12" fill="none" stroke="#E65100" stroke-width="3" stroke-linecap="round"/>
      <path d="M44 18v10c0 4-2 6-4 6" fill="none" stroke="#E65100" stroke-width="3" stroke-linecap="round"/>
      <path d="M41 18v10" fill="none" stroke="#E65100" stroke-width="3" stroke-linecap="round"/>
    </svg>""",

    "home": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
      <circle cx="32" cy="32" r="30" fill="#E3F2FD" stroke="#1565C0" stroke-width="3"/>
      <path d="M14 30L32 14L50 30" fill="none" stroke="#1565C0" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
      <rect x="20" y="30" width="24" height="18" rx="2" fill="none" stroke="#1565C0" stroke-width="3"/>
      <rect x="28" y="36" width="8" height="12" rx="1" fill="none" stroke="#1565C0" stroke-width="3"/>
    </svg>""",

    "transport": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
      <circle cx="32" cy="32" r="30" fill="#E8F5E9" stroke="#2E7D32" stroke-width="3"/>
      <rect x="12" y="22" width="40" height="18" rx="6" fill="none" stroke="#2E7D32" stroke-width="3"/>
      <path d="M12 32h40" stroke="#2E7D32" stroke-width="2"/>
      <circle cx="22" cy="44" r="4" fill="none" stroke="#2E7D32" stroke-width="3"/>
      <circle cx="42" cy="44" r="4" fill="none" stroke="#2E7D32" stroke-width="3"/>
      <path d="M38 22l4-8h6" fill="none" stroke="#2E7D32" stroke-width="2" stroke-linecap="round"/>
    </svg>""",

    "clothes": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
      <circle cx="32" cy="32" r="30" fill="#F3E5F5" stroke="#7B1FA2" stroke-width="3"/>
      <path d="M24 14L14 24l6 4v22h24V28l6-4L40 14" fill="none" stroke="#7B1FA2" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M24 14c0 4 3.6 8 8 8s8-4 8-8" fill="none" stroke="#7B1FA2" stroke-width="3"/>
    </svg>""",

    "fun": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
      <circle cx="32" cy="32" r="30" fill="#FFF9C4" stroke="#F57F17" stroke-width="3"/>
      <circle cx="32" cy="32" r="16" fill="none" stroke="#F57F17" stroke-width="3"/>
      <circle cx="26" cy="28" r="2" fill="#F57F17"/>
      <circle cx="38" cy="28" r="2" fill="#F57F17"/>
      <path d="M24 36c2 4 6 6 8 6s6-2 8-6" fill="none" stroke="#F57F17" stroke-width="2.5" stroke-linecap="round"/>
    </svg>""",

    "health": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
      <circle cx="32" cy="32" r="30" fill="#FFEBEE" stroke="#C62828" stroke-width="3"/>
      <path d="M32 46L18 30c-4-5-2-14 6-14 4 0 6 2 8 5 2-3 4-5 8-5 8 0 10 9 6 14z" fill="none" stroke="#C62828" stroke-width="3" stroke-linejoin="round"/>
    </svg>""",

    "other": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
      <circle cx="32" cy="32" r="30" fill="#ECEFF1" stroke="#455A64" stroke-width="3"/>
      <circle cx="22" cy="32" r="3" fill="#455A64"/>
      <circle cx="32" cy="32" r="3" fill="#455A64"/>
      <circle cx="42" cy="32" r="3" fill="#455A64"/>
    </svg>""",

    "money": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
      <circle cx="32" cy="32" r="30" fill="#E8F5E9" stroke="#2E7D32" stroke-width="3"/>
      <circle cx="32" cy="32" r="16" fill="none" stroke="#2E7D32" stroke-width="3"/>
      <text x="32" y="38" font-family="sans-serif" font-size="20" font-weight="bold" fill="#2E7D32" text-anchor="middle">kr</text>
    </svg>""",

    "warning": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
      <path d="M32 6L4 58h56z" fill="#FFF3E0" stroke="#E65100" stroke-width="3" stroke-linejoin="round"/>
      <line x1="32" y1="24" x2="32" y2="40" stroke="#E65100" stroke-width="4" stroke-linecap="round"/>
      <circle cx="32" cy="48" r="3" fill="#E65100"/>
    </svg>""",

    "happy": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
      <circle cx="32" cy="32" r="30" fill="#E8F5E9" stroke="#2E7D32" stroke-width="3"/>
      <circle cx="24" cy="26" r="3" fill="#2E7D32"/>
      <circle cx="40" cy="26" r="3" fill="#2E7D32"/>
      <path d="M20 38c3 6 8 8 12 8s9-2 12-8" fill="none" stroke="#2E7D32" stroke-width="3" stroke-linecap="round"/>
    </svg>""",

    "sad": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
      <circle cx="32" cy="32" r="30" fill="#FFEBEE" stroke="#C62828" stroke-width="3"/>
      <circle cx="24" cy="26" r="3" fill="#C62828"/>
      <circle cx="40" cy="26" r="3" fill="#C62828"/>
      <path d="M22 44c3-6 8-8 10-8s7 2 10 8" fill="none" stroke="#C62828" stroke-width="3" stroke-linecap="round"/>
    </svg>""",
}


def get_svg_bytes(icon_name):
    """Get SVG icon as bytes for GdkPixbuf/Texture loading."""
    svg = ICONS.get(icon_name, ICONS["other"])
    return svg.encode("utf-8")
