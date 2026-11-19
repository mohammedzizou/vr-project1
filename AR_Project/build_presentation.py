#!/usr/bin/env python3
"""
Build AR Presentation — PPTX Generator
Creates a professional university presentation about Augmented Reality.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ==============================================================================
# CONFIGURATION
# ==============================================================================

PROJECT_DIR = "/Users/mohamed/Downloads/AR_Project"
IMAGES_DIR = os.path.join(PROJECT_DIR, "presentation", "images")
OUTPUT_PPTX = os.path.join(PROJECT_DIR, "presentation", "AR_Presentation.pptx")

# Color scheme
DARK_BG = RGBColor(0x0A, 0x0E, 0x27)       # Very dark navy
DARK_BG2 = RGBColor(0x0F, 0x17, 0x3D)      # Slightly lighter navy
ACCENT_CYAN = RGBColor(0x00, 0xD4, 0xFF)    # Electric cyan
ACCENT_BLUE = RGBColor(0x38, 0x7A, 0xFF)    # Bright blue
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY = RGBColor(0xBB, 0xCC, 0xDD)
GREEN = RGBColor(0x00, 0xE6, 0x96)          # Mint green for advantages
AMBER = RGBColor(0xFF, 0xB7, 0x4D)          # Amber for limitations
PURPLE = RGBColor(0xA855, 0xF7, 0x00)[0:3] if False else RGBColor(0xA8, 0x55, 0xF7)  # Purple for VR


# Slide dimensions (16:9 widescreen)
SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)


def create_gradient_background(slide, color1_rgb, color2_rgb=None):
    """Add a solid dark background to the slide."""
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color1_rgb


def add_shape_bg(slide, left, top, width, height, color, alpha=255):
    """Add a semi-transparent colored rectangle."""
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    # Set transparency if needed
    if alpha < 255:
        shape.fill.fore_color.brightness = 0
    return shape


def add_text_box(slide, left, top, width, height, text, font_size=18,
                 bold=False, color=WHITE, alignment=PP_ALIGN.LEFT,
                 font_name="Calibri"):
    """Add a text box to the slide."""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.font.name = font_name
    p.alignment = alignment
    return txBox


def add_multi_text(slide, left, top, width, height, lines, default_size=18,
                   default_color=WHITE, font_name="Calibri", line_spacing=1.5):
    """Add a text box with multiple styled lines.
    lines = [(text, font_size, bold, color, alignment), ...]
    """
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True

    for i, line_data in enumerate(lines):
        text = line_data[0]
        size = line_data[1] if len(line_data) > 1 else default_size
        bold = line_data[2] if len(line_data) > 2 else False
        color = line_data[3] if len(line_data) > 3 else default_color
        align = line_data[4] if len(line_data) > 4 else PP_ALIGN.LEFT

        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()

        p.text = text
        p.font.size = Pt(size)
        p.font.bold = bold
        p.font.color.rgb = color
        p.font.name = font_name
        p.alignment = align
        p.space_after = Pt(4)

    return txBox


def add_bullet_list(slide, left, top, width, height, items, font_size=16,
                    color=WHITE, bullet_color=ACCENT_CYAN, font_name="Calibri"):
    """Add a bulleted list."""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True

    for i, item in enumerate(items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()

        # Use bullet character
        run1 = p.add_run()
        run1.text = "● "
        run1.font.size = Pt(font_size)
        run1.font.color.rgb = bullet_color
        run1.font.name = font_name

        run2 = p.add_run()
        run2.text = item
        run2.font.size = Pt(font_size)
        run2.font.color.rgb = color
        run2.font.name = font_name

        p.space_after = Pt(6)

    return txBox


def add_slide_number(slide, number, total=7):
    """Add slide number to bottom right."""
    add_text_box(
        slide, Inches(11.5), Inches(6.9), Inches(1.5), Inches(0.4),
        f"{number} / {total}", font_size=10, color=LIGHT_GRAY,
        alignment=PP_ALIGN.RIGHT
    )


def add_accent_line(slide, left, top, width):
    """Add a colored accent line."""
    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, left, top, width, Pt(3)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = ACCENT_CYAN
    shape.line.fill.background()
    return shape


def try_add_image(slide, image_name, left, top, width, height=None):
    """Try to add an image. If not found, add a placeholder shape instead."""
    image_path = os.path.join(IMAGES_DIR, image_name)
    if os.path.exists(image_path):
        if height:
            slide.shapes.add_picture(image_path, left, top, width, height)
        else:
            slide.shapes.add_picture(image_path, left, top, width)
        return True
    return False


def generate_missing_images():
    """Skip placeholder generation — missing images will show shapes instead."""
    missing = []
    needed = [
        "slide1_title.jpg", "slide2_what_is_ar.jpg", "slide3_ar_vs_vr.jpg",
        "slide4_how_ar_works.jpg", "slide5_ar_types.jpg",
        "slide5_applications.jpg", "slide6_pros_cons.jpg", "slide7_ar_demo.jpg"
    ]
    for f in needed:
        path = os.path.join(IMAGES_DIR, f)
        if not os.path.exists(path):
            missing.append(f)
    if missing:
        print(f"  ⚠️  Missing images (will use shapes): {', '.join(missing)}")
    else:
        print("  ✅ All images found")


# ==============================================================================
# SLIDE BUILDERS
# ==============================================================================

def build_slide_1_title(prs):
    """Slide 1 — Title / Introduction"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout
    create_gradient_background(slide, DARK_BG)

    # Try to add background image
    img_path = os.path.join(IMAGES_DIR, "slide1_title.jpg")
    if os.path.exists(img_path):
        slide.shapes.add_picture(img_path, Inches(0), Inches(0), SLIDE_WIDTH, SLIDE_HEIGHT)

    # Dark overlay for readability
    overlay = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), SLIDE_WIDTH, SLIDE_HEIGHT
    )
    overlay.fill.solid()
    overlay.fill.fore_color.rgb = RGBColor(0x0A, 0x0E, 0x27)
    # Make semi-transparent by adjusting alpha
    overlay.fill.fore_color.brightness = 0.0
    overlay.line.fill.background()

    # Title
    add_text_box(
        slide, Inches(1), Inches(1.5), Inches(11), Inches(1.2),
        "AUGMENTED REALITY", font_size=52, bold=True,
        color=WHITE, alignment=PP_ALIGN.CENTER, font_name="Calibri"
    )

    # Accent line
    add_accent_line(slide, Inches(4.5), Inches(2.8), Inches(4))

    # Subtitle
    add_text_box(
        slide, Inches(1.5), Inches(3.1), Inches(10), Inches(0.8),
        "Understanding the Technology and Its Real-World Applications",
        font_size=24, bold=False, color=ACCENT_CYAN,
        alignment=PP_ALIGN.CENTER
    )

    # Student info
    add_multi_text(
        slide, Inches(3.5), Inches(4.5), Inches(6), Inches(1.5),
        [
            ("Presented by: [Your Name]", 16, False, LIGHT_GRAY, PP_ALIGN.CENTER),
            ("Master's Program — [University Name]", 14, False, LIGHT_GRAY, PP_ALIGN.CENTER),
            ("November 2026", 14, False, LIGHT_GRAY, PP_ALIGN.CENTER),
        ]
    )

    # Topic preview box
    box = add_shape_bg(slide, Inches(3), Inches(5.8), Inches(7), Inches(1.2),
                       RGBColor(0x14, 0x1E, 0x4A))
    add_multi_text(
        slide, Inches(3.3), Inches(5.9), Inches(6.4), Inches(1.0),
        [
            ("Today's Topics:", 13, True, ACCENT_CYAN, PP_ALIGN.CENTER),
            ("Definition  •  AR vs VR  •  How It Works  •  Types & Apps  •  Pros & Cons  •  Live Demo",
             11, False, LIGHT_GRAY, PP_ALIGN.CENTER),
        ]
    )

    add_slide_number(slide, 1)

    # Speaker notes
    notes_slide = slide.notes_slide
    notes_slide.notes_text_frame.text = (
        "Good morning everyone. Thank you for being here today.\n\n"
        "My name is [YOUR NAME], and I am a Master's student at [YOUR UNIVERSITY].\n\n"
        "Today, I will talk about a very interesting technology called Augmented Reality, or simply AR.\n\n"
        "By the end of this presentation, you will understand exactly what AR is, how it works, "
        "and where it is used in real life.\n\n"
        "I will cover six main topics: definition, AR vs VR, how it works, types and applications, "
        "advantages and limitations, and finally a live demo.\n\n"
        "Let's begin."
    )

    print("  ✅ Slide 1 — Title")


def build_slide_2_definition(prs):
    """Slide 2 — What is Augmented Reality?"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    create_gradient_background(slide, DARK_BG)

    # Section label
    add_text_box(
        slide, Inches(0.8), Inches(0.3), Inches(4), Inches(0.4),
        "01 — DEFINITION", font_size=12, bold=True, color=ACCENT_CYAN
    )

    # Title
    add_text_box(
        slide, Inches(0.8), Inches(0.6), Inches(6), Inches(0.8),
        "What is Augmented Reality?", font_size=36, bold=True, color=WHITE
    )
    add_accent_line(slide, Inches(0.8), Inches(1.4), Inches(3))

    # Definition box
    def_box = add_shape_bg(slide, Inches(0.8), Inches(1.7), Inches(5.5), Inches(1.2),
                            RGBColor(0x14, 0x1E, 0x4A))
    add_multi_text(
        slide, Inches(1.1), Inches(1.8), Inches(5), Inches(1.0),
        [
            ('"Augmented" means "to add" or "to enhance"', 13, True, ACCENT_CYAN),
            ("", 6),
            ("AR adds digital content — images, sounds,", 15, False, WHITE),
            ("or 3D objects — on top of the real world.", 15, False, WHITE),
        ]
    )

    # Three examples
    add_text_box(
        slide, Inches(0.8), Inches(3.2), Inches(5), Inches(0.4),
        "Everyday Examples:", font_size=18, bold=True, color=WHITE
    )

    examples = [
        "📱  Snapchat & Instagram Filters — digital effects on your face",
        "🎮  Pokémon GO — virtual creatures on real streets",
        "🛋️  IKEA Place — virtual furniture in your real room",
    ]
    add_bullet_list(
        slide, Inches(0.8), Inches(3.7), Inches(5.5), Inches(2.5),
        examples, font_size=15, color=LIGHT_GRAY
    )

    # Key point box
    key_box = add_shape_bg(slide, Inches(0.8), Inches(6.0), Inches(5.5), Inches(0.8),
                            RGBColor(0x0C, 0x2A, 0x1A))
    add_text_box(
        slide, Inches(1.1), Inches(6.1), Inches(5), Inches(0.6),
        "💡 Key Point: You see the real world + digital content at the same time",
        font_size=14, bold=True, color=GREEN
    )

    # Image on right side
    img_added = try_add_image(slide, "slide2_what_is_ar.jpg",
                               Inches(6.8), Inches(0.8), Inches(6), Inches(5.8))

    add_slide_number(slide, 2)

    # Speaker notes
    notes_slide = slide.notes_slide
    notes_slide.notes_text_frame.text = (
        "So, what is Augmented Reality?\n\n"
        "Let me give you a simple definition:\n"
        "AR is a technology that adds digital content — like images, sounds, or 3D objects — "
        "on top of the real world.\n\n"
        "The key word is 'augmented.' It means 'to add' or 'to enhance.'\n\n"
        "Example 1 — Snapchat Filters: When you see dog ears on your face, that is AR.\n"
        "Example 2 — Pokémon GO: You see a Pokémon on the street through your phone.\n"
        "Example 3 — IKEA Place: You can see virtual furniture in your room before buying.\n\n"
        "To summarize: AR takes the real world and adds digital things on top of it."
    )

    print("  ✅ Slide 2 — Definition")


def build_slide_3_ar_vs_vr(prs):
    """Slide 3 — AR vs VR Comparison"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    create_gradient_background(slide, DARK_BG)

    # Section label
    add_text_box(
        slide, Inches(0.8), Inches(0.3), Inches(4), Inches(0.4),
        "02 — COMPARISON", font_size=12, bold=True, color=ACCENT_CYAN
    )

    # Title
    add_text_box(
        slide, Inches(0.8), Inches(0.6), Inches(11), Inches(0.8),
        "Augmented Reality  vs  Virtual Reality", font_size=36, bold=True, color=WHITE
    )
    add_accent_line(slide, Inches(0.8), Inches(1.4), Inches(3))

    # Image
    try_add_image(slide, "slide3_ar_vs_vr.jpg",
                  Inches(0.8), Inches(1.7), Inches(6), Inches(3.4))

    # Comparison table area
    table_left = Inches(7.2)

    # AR Column header
    ar_box = add_shape_bg(slide, table_left, Inches(1.7), Inches(2.6), Inches(0.5),
                           RGBColor(0x00, 0x3D, 0x5C))
    add_text_box(slide, table_left + Inches(0.1), Inches(1.75), Inches(2.4), Inches(0.4),
                 "🔵 Augmented Reality", font_size=14, bold=True, color=ACCENT_CYAN,
                 alignment=PP_ALIGN.CENTER)

    # VR Column header
    vr_box = add_shape_bg(slide, table_left + Inches(2.8), Inches(1.7), Inches(2.6), Inches(0.5),
                           RGBColor(0x2D, 0x1B, 0x4E))
    add_text_box(slide, table_left + Inches(2.9), Inches(1.75), Inches(2.4), Inches(0.4),
                 "🟣 Virtual Reality", font_size=14, bold=True, color=PURPLE,
                 alignment=PP_ALIGN.CENTER)

    # Comparison rows
    rows = [
        ("What You See", "Real world + digital content", "Only a virtual world"),
        ("Device", "Smartphone or AR glasses", "Full VR headset"),
        ("Immersion", "Partial — you see reality", "Full — reality is hidden"),
        ("Examples", "Snapchat, Pokémon GO,\nGoogle Maps Live View", "Meta Quest, PlayStation VR,\nFlight simulators"),
        ("Movement", "Move freely in real world", "Limited to a small area"),
    ]

    for i, (label, ar_val, vr_val) in enumerate(rows):
        y = Inches(2.35) + Inches(i * 0.72)
        row_color = RGBColor(0x14, 0x1E, 0x4A) if i % 2 == 0 else RGBColor(0x10, 0x18, 0x3E)

        # Row background
        add_shape_bg(slide, table_left, y, Inches(5.4), Inches(0.65), row_color)

        # Label
        add_text_box(slide, table_left + Inches(0.1), y + Inches(0.05),
                     Inches(1.4), Inches(0.55),
                     label, font_size=11, bold=True, color=LIGHT_GRAY)

        # AR value
        add_text_box(slide, table_left + Inches(1.3), y + Inches(0.05),
                     Inches(1.9), Inches(0.55),
                     ar_val, font_size=11, color=WHITE)

        # VR value
        add_text_box(slide, table_left + Inches(3.3), y + Inches(0.05),
                     Inches(2.0), Inches(0.55),
                     vr_val, font_size=11, color=WHITE)

    # Key takeaway
    key_box = add_shape_bg(slide, Inches(0.8), Inches(6.0), Inches(11.5), Inches(0.8),
                            RGBColor(0x0C, 0x2A, 0x1A))
    add_text_box(
        slide, Inches(1.1), Inches(6.1), Inches(11), Inches(0.6),
        "💡 Remember:  AR adds to your reality  |  VR replaces your reality",
        font_size=16, bold=True, color=GREEN, alignment=PP_ALIGN.CENTER
    )

    add_slide_number(slide, 3)

    # Speaker notes
    notes_slide = slide.notes_slide
    notes_slide.notes_text_frame.text = (
        "Many people confuse AR with VR. They sound similar, but they are very different.\n\n"
        "AR adds digital things to the real world. You can still see everything around you.\n"
        "VR replaces the real world completely. When you wear a VR headset, you cannot see the room.\n\n"
        "Think of it this way:\n"
        "AR is like looking through a window and seeing extra information on the glass.\n"
        "VR is like closing your eyes and entering a dream.\n\n"
        "The easiest way to remember: AR adds to reality. VR replaces reality."
    )

    print("  ✅ Slide 3 — AR vs VR")


def build_slide_4_how_it_works(prs):
    """Slide 4 — How AR Works"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    create_gradient_background(slide, DARK_BG)

    # Section label
    add_text_box(
        slide, Inches(0.8), Inches(0.3), Inches(4), Inches(0.4),
        "03 — HOW IT WORKS", font_size=12, bold=True, color=ACCENT_CYAN
    )

    # Title
    add_text_box(
        slide, Inches(0.8), Inches(0.6), Inches(11), Inches(0.8),
        "How Does AR Work?", font_size=36, bold=True, color=WHITE
    )
    add_accent_line(slide, Inches(0.8), Inches(1.4), Inches(3))

    # Subtitle
    add_text_box(
        slide, Inches(0.8), Inches(1.6), Inches(11), Inches(0.5),
        "Four Simple Steps — From Camera to Screen", font_size=16, color=LIGHT_GRAY
    )

    # Four step cards
    steps = [
        ("1", "📷", "CAPTURE", "Camera captures\nthe real world", ACCENT_CYAN),
        ("2", "🔍", "DETECT", "Software finds surfaces,\nmarkers, or faces", ACCENT_BLUE),
        ("3", "⚙️", "PROCESS", "Computer calculates\nposition & angle", PURPLE),
        ("4", "📱", "DISPLAY", "Screen shows real world\n+ digital content", GREEN),
    ]

    card_width = Inches(2.6)
    card_height = Inches(2.8)
    start_x = Inches(0.8)
    gap = Inches(0.35)
    y_top = Inches(2.3)

    for i, (num, icon, title, desc, color) in enumerate(steps):
        x = start_x + (card_width + gap) * i

        # Card background
        card = add_shape_bg(slide, x, y_top, card_width, card_height,
                             RGBColor(0x14, 0x1E, 0x4A))

        # Step number circle
        circle = slide.shapes.add_shape(
            MSO_SHAPE.OVAL, x + Inches(0.9), y_top + Inches(0.2),
            Inches(0.7), Inches(0.7)
        )
        circle.fill.solid()
        circle.fill.fore_color.rgb = color
        circle.line.fill.background()

        # Number text on circle
        tf = circle.text_frame
        tf.word_wrap = False
        p = tf.paragraphs[0]
        p.text = num
        p.font.size = Pt(24)
        p.font.bold = True
        p.font.color.rgb = DARK_BG
        p.font.name = "Calibri"
        p.alignment = PP_ALIGN.CENTER

        # Step title
        add_text_box(slide, x + Inches(0.1), y_top + Inches(1.1),
                     card_width - Inches(0.2), Inches(0.4),
                     title, font_size=16, bold=True, color=color,
                     alignment=PP_ALIGN.CENTER)

        # Step description
        add_text_box(slide, x + Inches(0.1), y_top + Inches(1.6),
                     card_width - Inches(0.2), Inches(1.0),
                     desc, font_size=13, color=LIGHT_GRAY,
                     alignment=PP_ALIGN.CENTER)

    # Arrow connectors between cards
    for i in range(3):
        x_arrow = start_x + (card_width + gap) * (i + 1) - Inches(0.22)
        arrow = add_text_box(slide, x_arrow, y_top + Inches(1.0),
                              Inches(0.4), Inches(0.5),
                              "→", font_size=28, bold=True, color=ACCENT_CYAN,
                              alignment=PP_ALIGN.CENTER)

    # Pokémon GO example box
    example_box = add_shape_bg(slide, Inches(0.8), Inches(5.4), Inches(11.5), Inches(1.5),
                                RGBColor(0x14, 0x1E, 0x4A))
    add_text_box(
        slide, Inches(1.1), Inches(5.5), Inches(3), Inches(0.4),
        "📱 Real Example — Pokémon GO:", font_size=14, bold=True, color=ACCENT_CYAN
    )
    example_steps = [
        "1. Phone camera sees the street  →  2. Software detects the flat ground",
        "3. Computer calculates where to place the Pokémon  →  4. Screen shows the Pokémon on the street"
    ]
    add_multi_text(
        slide, Inches(1.1), Inches(5.95), Inches(10.5), Inches(0.9),
        [
            (example_steps[0], 13, False, LIGHT_GRAY),
            (example_steps[1], 13, False, LIGHT_GRAY),
        ]
    )

    add_slide_number(slide, 4)

    # Speaker notes
    notes_slide = slide.notes_slide
    notes_slide.notes_text_frame.text = (
        "Now I will explain how AR works. I will keep it simple.\n\n"
        "Step 1 — CAPTURE: Everything starts with a camera. It captures the real world.\n\n"
        "Step 2 — DETECT: The software looks for something specific — a marker, a surface, or a face.\n"
        "Think of it like this: if I want to put a virtual cup on a table, the software first needs to find the table.\n\n"
        "Step 3 — PROCESS: The computer calculates exactly where to place the digital object. "
        "It figures out the correct position, size, and angle.\n\n"
        "Step 4 — DISPLAY: The screen shows the real world combined with the digital object.\n\n"
        "Example — Pokémon GO:\n"
        "Camera sees the street → Software detects the ground → Computer places the Pokémon → Screen shows it."
    )

    print("  ✅ Slide 4 — How AR Works")


def build_slide_5_types_apps(prs):
    """Slide 5 — Types and Real-World Applications"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    create_gradient_background(slide, DARK_BG)

    # Section label
    add_text_box(
        slide, Inches(0.8), Inches(0.3), Inches(4), Inches(0.4),
        "04 — TYPES & APPLICATIONS", font_size=12, bold=True, color=ACCENT_CYAN
    )

    # Title
    add_text_box(
        slide, Inches(0.8), Inches(0.6), Inches(11), Inches(0.8),
        "Types & Real-World Applications", font_size=36, bold=True, color=WHITE
    )
    add_accent_line(slide, Inches(0.8), Inches(1.4), Inches(3))

    # Four types — left column
    types_data = [
        ("📌 Marker-Based", "Uses a printed image (marker)\nto place 3D content", "Museums, textbooks", ACCENT_CYAN),
        ("📍 Markerless", "Detects surfaces using sensors\n(no marker needed)", "IKEA Place, furniture apps", ACCENT_BLUE),
        ("💡 Projection-Based", "Projects digital images onto\nreal surfaces", "Virtual keyboards, factories", PURPLE),
        ("🔄 Superimposition", "Replaces part of real object\nwith digital version", "Medical X-ray views", AMBER),
    ]

    add_text_box(
        slide, Inches(0.8), Inches(1.6), Inches(5), Inches(0.4),
        "4 Types of AR", font_size=18, bold=True, color=WHITE
    )

    for i, (name, desc, example, color) in enumerate(types_data):
        y = Inches(2.1) + Inches(i * 1.1)
        card = add_shape_bg(slide, Inches(0.8), y, Inches(5.5), Inches(0.95),
                             RGBColor(0x14, 0x1E, 0x4A))
        add_text_box(slide, Inches(1.0), y + Inches(0.05),
                     Inches(2.5), Inches(0.35),
                     name, font_size=14, bold=True, color=color)
        add_text_box(slide, Inches(1.0), y + Inches(0.35),
                     Inches(3.0), Inches(0.55),
                     desc, font_size=11, color=LIGHT_GRAY)
        add_text_box(slide, Inches(4.0), y + Inches(0.35),
                     Inches(2.2), Inches(0.55),
                     f"Ex: {example}", font_size=10, color=color)

    # Applications — right column
    add_text_box(
        slide, Inches(7.0), Inches(1.6), Inches(5), Inches(0.4),
        "Real-World Applications", font_size=18, bold=True, color=WHITE
    )

    apps_data = [
        ("🏥 Medicine", "Surgery guidance, patient data overlay"),
        ("📚 Education", "3D anatomy, interactive solar system"),
        ("🛒 Retail", "Virtual try-on, furniture preview"),
        ("🗺️ Navigation", "Google Maps Live View — AR arrows"),
        ("🎮 Gaming", "Pokémon GO, AR escape rooms"),
        ("🏭 Industry", "Hands-free repair instructions"),
    ]

    for i, (field, desc) in enumerate(apps_data):
        y = Inches(2.1) + Inches(i * 0.8)
        card = add_shape_bg(slide, Inches(7.0), y, Inches(5.5), Inches(0.7),
                             RGBColor(0x14, 0x1E, 0x4A))
        add_text_box(slide, Inches(7.2), y + Inches(0.05),
                     Inches(2.0), Inches(0.3),
                     field, font_size=14, bold=True, color=GREEN)
        add_text_box(slide, Inches(7.2), y + Inches(0.33),
                     Inches(5.0), Inches(0.35),
                     desc, font_size=12, color=LIGHT_GRAY)

    add_slide_number(slide, 5)

    # Speaker notes
    notes_slide = slide.notes_slide
    notes_slide.notes_text_frame.text = (
        "There are four main types of AR.\n\n"
        "Type 1 — Marker-Based: Uses a printed image. When the camera sees the marker, "
        "it shows a 3D object on top. Example: museum displays.\n\n"
        "Type 2 — Markerless: Does not need a marker. It detects flat surfaces. "
        "Example: IKEA Place app.\n\n"
        "Type 3 — Projection-Based: Uses a projector to display on real surfaces. "
        "Example: virtual keyboards.\n\n"
        "Type 4 — Superimposition: Replaces part of a real object with digital version. "
        "Example: medical X-ray view.\n\n"
        "Applications: Medicine (surgery), Education (3D models), Retail (virtual try-on), "
        "Navigation (Google Maps AR), Gaming (Pokémon GO), Industry (maintenance)."
    )

    print("  ✅ Slide 5 — Types & Applications")


def build_slide_6_pros_cons(prs):
    """Slide 6 — Advantages and Limitations"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    create_gradient_background(slide, DARK_BG)

    # Section label
    add_text_box(
        slide, Inches(0.8), Inches(0.3), Inches(6), Inches(0.4),
        "05 — ADVANTAGES & LIMITATIONS", font_size=12, bold=True, color=ACCENT_CYAN
    )

    # Title
    add_text_box(
        slide, Inches(0.8), Inches(0.6), Inches(11), Inches(0.8),
        "Advantages & Limitations", font_size=36, bold=True, color=WHITE
    )
    add_accent_line(slide, Inches(0.8), Inches(1.4), Inches(3))

    # === ADVANTAGES (left side) ===
    adv_header_box = add_shape_bg(slide, Inches(0.8), Inches(1.7), Inches(5.5), Inches(0.6),
                                   RGBColor(0x0C, 0x2A, 0x1A))
    add_text_box(slide, Inches(1.0), Inches(1.75), Inches(5), Inches(0.5),
                 "✅  Advantages", font_size=20, bold=True, color=GREEN,
                 alignment=PP_ALIGN.CENTER)

    advantages = [
        ("💡 Interactive Learning", "Students learn more by seeing 3D\nmodels instead of flat images"),
        ("🙌 Hands-Free Information", "Workers see instructions while\nkeeping their hands free"),
        ("🛍️ Better Shopping", "Try products virtually before\nbuying — saves time & money"),
        ("🛡️ Safer Training", "Practice dangerous tasks in a\nsafe virtual environment"),
    ]

    for i, (title, desc) in enumerate(advantages):
        y = Inches(2.5) + Inches(i * 1.1)
        card = add_shape_bg(slide, Inches(0.8), y, Inches(5.5), Inches(0.95),
                             RGBColor(0x0E, 0x22, 0x18))
        add_text_box(slide, Inches(1.0), y + Inches(0.08),
                     Inches(5), Inches(0.35),
                     title, font_size=15, bold=True, color=GREEN)
        add_text_box(slide, Inches(1.0), y + Inches(0.42),
                     Inches(5), Inches(0.5),
                     desc, font_size=12, color=LIGHT_GRAY)

    # === LIMITATIONS (right side) ===
    lim_header_box = add_shape_bg(slide, Inches(7.0), Inches(1.7), Inches(5.5), Inches(0.6),
                                   RGBColor(0x2A, 0x1A, 0x0C))
    add_text_box(slide, Inches(7.2), Inches(1.75), Inches(5), Inches(0.5),
                 "⚠️  Limitations", font_size=20, bold=True, color=AMBER,
                 alignment=PP_ALIGN.CENTER)

    limitations = [
        ("🔋 Battery Consumption", "AR uses camera + processor + screen\nat the same time — drains battery fast"),
        ("👁️ Privacy Concerns", "AR cameras can record people\nwithout their knowledge"),
        ("💰 Expensive Hardware", "Good AR glasses cost $3,000+\n(e.g., Microsoft HoloLens)"),
        ("📐 Limited Field of View", "Current AR glasses show digital\ncontent in a small area only"),
    ]

    for i, (title, desc) in enumerate(limitations):
        y = Inches(2.5) + Inches(i * 1.1)
        card = add_shape_bg(slide, Inches(7.0), y, Inches(5.5), Inches(0.95),
                             RGBColor(0x2A, 0x1E, 0x0E))
        add_text_box(slide, Inches(7.2), y + Inches(0.08),
                     Inches(5), Inches(0.35),
                     title, font_size=15, bold=True, color=AMBER)
        add_text_box(slide, Inches(7.2), y + Inches(0.42),
                     Inches(5), Inches(0.5),
                     desc, font_size=12, color=LIGHT_GRAY)

    add_slide_number(slide, 6)

    # Speaker notes
    notes_slide = slide.notes_slide
    notes_slide.notes_text_frame.text = (
        "Like any technology, AR has advantages and limitations.\n\n"
        "ADVANTAGES:\n"
        "1. Interactive Learning — AR makes learning visual. Students remember more.\n"
        "2. Hands-Free Info — Workers and doctors see info without using their hands.\n"
        "3. Better Shopping — Try furniture, clothes, makeup virtually.\n"
        "4. Safer Training — Practice dangerous situations safely.\n\n"
        "LIMITATIONS:\n"
        "1. Battery — AR uses camera, processor, and screen simultaneously.\n"
        "2. Privacy — AR cameras may record without permission.\n"
        "3. Cost — HoloLens costs $3,000+. Too expensive for many.\n"
        "4. Field of View — Digital content appears in a small area only."
    )

    print("  ✅ Slide 6 — Advantages & Limitations")


def build_slide_7_demo_conclusion(prs):
    """Slide 7 — Practical Demo & Conclusion"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    create_gradient_background(slide, DARK_BG)

    # Section label
    add_text_box(
        slide, Inches(0.8), Inches(0.3), Inches(6), Inches(0.4),
        "06 — LIVE DEMO & CONCLUSION", font_size=12, bold=True, color=ACCENT_CYAN
    )

    # Title
    add_text_box(
        slide, Inches(0.8), Inches(0.6), Inches(11), Inches(0.8),
        "🌍 AR Solar System Demo", font_size=36, bold=True, color=WHITE
    )
    add_accent_line(slide, Inches(0.8), Inches(1.4), Inches(3))

    # Demo explanation box — left side
    add_text_box(
        slide, Inches(0.8), Inches(1.6), Inches(5.5), Inches(0.4),
        "How the Demo Works:", font_size=18, bold=True, color=ACCENT_CYAN
    )

    demo_steps = [
        "1️⃣  Print the Hiro marker on paper",
        "2️⃣  Open the AR app on your phone",
        "3️⃣  Point your camera at the marker",
        "4️⃣  Watch the 3D solar system appear!",
    ]

    for i, step in enumerate(demo_steps):
        y = Inches(2.1) + Inches(i * 0.55)
        step_box = add_shape_bg(slide, Inches(0.8), y, Inches(5.5), Inches(0.45),
                                 RGBColor(0x14, 0x1E, 0x4A))
        add_text_box(slide, Inches(1.0), y + Inches(0.05),
                     Inches(5), Inches(0.35),
                     step, font_size=15, bold=False, color=WHITE)

    # Technology note
    tech_box = add_shape_bg(slide, Inches(0.8), Inches(4.4), Inches(5.5), Inches(0.6),
                             RGBColor(0x0C, 0x2A, 0x1A))
    add_text_box(slide, Inches(1.0), Inches(4.45), Inches(5), Inches(0.5),
                 "Built with: A-Frame (3D) + AR.js (AR) — runs in any browser!",
                 font_size=12, bold=False, color=GREEN)

    # Image on right side
    try_add_image(slide, "slide7_ar_demo.jpg",
                  Inches(6.8), Inches(1.6), Inches(5.8), Inches(3.5))

    # Conclusion / Key Takeaways
    conc_header = add_shape_bg(slide, Inches(0.8), Inches(5.2), Inches(11.5), Inches(0.5),
                                RGBColor(0x14, 0x1E, 0x4A))
    add_text_box(slide, Inches(1.0), Inches(5.25), Inches(11), Inches(0.4),
                 "📋  Key Takeaways", font_size=18, bold=True, color=ACCENT_CYAN,
                 alignment=PP_ALIGN.CENTER)

    takeaways = [
        ("1", "AR adds digital content to the real world"),
        ("2", "AR ≠ VR — AR adds, VR replaces"),
        ("3", "4 steps: Capture → Detect → Process → Display"),
        ("4", "Used in medicine, education, retail, gaming, navigation, industry"),
        ("5", "Powerful but still has limitations (battery, cost, privacy)"),
    ]

    for i, (num, text) in enumerate(takeaways):
        x = Inches(0.8) + Inches(i * 2.35)
        y = Inches(5.85)
        tk_box = add_shape_bg(slide, x, y, Inches(2.2), Inches(1.0),
                               RGBColor(0x0E, 0x22, 0x18))

        # Number circle
        circle = slide.shapes.add_shape(
            MSO_SHAPE.OVAL, x + Inches(0.75), y + Inches(0.08),
            Inches(0.45), Inches(0.45)
        )
        circle.fill.solid()
        circle.fill.fore_color.rgb = ACCENT_CYAN
        circle.line.fill.background()
        tf = circle.text_frame
        p = tf.paragraphs[0]
        p.text = num
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = DARK_BG
        p.font.name = "Calibri"
        p.alignment = PP_ALIGN.CENTER

        add_text_box(slide, x + Inches(0.1), y + Inches(0.55),
                     Inches(2.0), Inches(0.45),
                     text, font_size=9, color=LIGHT_GRAY,
                     alignment=PP_ALIGN.CENTER)

    # Thank you
    add_text_box(
        slide, Inches(1), Inches(6.95), Inches(11), Inches(0.4),
        "Thank you! Questions?  ·  📧 [your.email@university.com]",
        font_size=12, color=LIGHT_GRAY, alignment=PP_ALIGN.CENTER
    )

    add_slide_number(slide, 7)

    # Speaker notes
    notes_slide = slide.notes_slide
    notes_slide.notes_text_frame.text = (
        "For the last part, I will show you a real AR example.\n\n"
        "I created a simple AR Solar System using AR.js. It is marker-based AR.\n\n"
        "Demo steps:\n"
        "1. I have a printed marker — the Hiro marker.\n"
        "2. I open the AR app on my phone browser.\n"
        "3. I point the camera at the marker.\n"
        "4. A 3D solar system appears with rotating planets.\n\n"
        "[DO THE LIVE DEMO HERE]\n\n"
        "CONCLUSION — Today we learned 5 things:\n"
        "1. AR adds digital content to the real world.\n"
        "2. AR is different from VR — AR adds, VR replaces.\n"
        "3. AR works in 4 steps: Camera, Detect, Process, Display.\n"
        "4. 4 types of AR — used in medicine, education, retail, gaming, etc.\n"
        "5. AR has great advantages but also limitations.\n\n"
        "Thank you for your attention. I am happy to answer any questions."
    )

    print("  ✅ Slide 7 — Demo & Conclusion")


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    print("\n🎯 Building AR Presentation...\n")

    # Generate placeholder images for missing ones
    print("📸 Checking images...")
    generate_missing_images()

    # Create presentation (16:9 widescreen)
    prs = Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT

    # Build all slides
    print("\n📊 Building slides...")
    build_slide_1_title(prs)
    build_slide_2_definition(prs)
    build_slide_3_ar_vs_vr(prs)
    build_slide_4_how_it_works(prs)
    build_slide_5_types_apps(prs)
    build_slide_6_pros_cons(prs)
    build_slide_7_demo_conclusion(prs)

    # Save PPTX
    prs.save(OUTPUT_PPTX)
    print(f"\n✅ Presentation saved: {OUTPUT_PPTX}")
    print(f"   📁 Total slides: {len(prs.slides)}")
    print(f"   📐 Format: 16:9 Widescreen")

    # File size
    file_size = os.path.getsize(OUTPUT_PPTX)
    print(f"   📦 File size: {file_size / 1024:.0f} KB")

    print("\n🎉 Done! Open the PPTX file in PowerPoint or Google Slides.")
    print("   You can also export to PDF from PowerPoint: File → Export → PDF")


if __name__ == "__main__":
    main()
