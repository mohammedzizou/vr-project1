#!/usr/bin/env python3
"""
Generate AR Presentation PDF using fpdf2
Creates a high-resolution, landscape 16:9 PDF presentation matching the 7 slides.
"""

import os
from fpdf import FPDF

PROJECT_DIR = "/Users/mohamed/Downloads/AR_Project"
IMAGES_DIR = os.path.join(PROJECT_DIR, "presentation", "images")
OUTPUT_PDF = os.path.join(PROJECT_DIR, "presentation", "AR_Presentation.pdf")

# Palette constants
NAVY_BG = (10, 14, 39)        # #0A0E27
CARD_BG = (19, 28, 64)        # #131C40
CARD_BORDER = (38, 56, 110)
CYAN = (0, 212, 255)          # #00D4FF
BLUE = (56, 122, 255)         # #387AFF
GREEN = (0, 230, 150)         # #00E696
AMBER = (255, 183, 77)        # #FFB74D
PURPLE = (168, 85, 247)       # #A855F7
WHITE = (255, 255, 255)
LIGHT_GRAY = (187, 204, 221)
MUTED_GRAY = (130, 150, 180)

class ARPresentationPDF(FPDF):
    def __init__(self):
        # 16:9 landscape (297 mm x 167 mm)
        super().__init__(orientation="L", unit="mm", format=(167.06, 297.0))
        self.set_auto_page_break(auto=False)

    def draw_background(self):
        self.set_fill_color(*NAVY_BG)
        self.rect(0, 0, 297, 167.06, style="F")

    def draw_card(self, x, y, w, h, fill=CARD_BG, border=CARD_BORDER, r=3):
        self.set_fill_color(*fill)
        if border:
            self.set_draw_color(*border)
            self.set_line_width(0.4)
            self.rect(x, y, w, h, style="FD", round_corners=True, corner_radius=r)
        else:
            self.rect(x, y, w, h, style="F", round_corners=True, corner_radius=r)

    def draw_header(self, slide_num, title, subtitle=None):
        # Top banner category
        self.set_xy(16, 12)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*CYAN)
        self.cell(200, 6, f"SLIDE {slide_num} / 7", ln=False)

        # Title
        self.set_xy(16, 18)
        self.set_font("Helvetica", "B", 20)
        self.set_text_color(*WHITE)
        self.cell(200, 10, title, ln=False)

        # Subtitle
        if subtitle:
            self.set_xy(16, 28)
            self.set_font("Helvetica", "", 11)
            self.set_text_color(*LIGHT_GRAY)
            self.cell(200, 6, subtitle, ln=False)

    def draw_footer(self, slide_num):
        self.set_xy(16, 156)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*MUTED_GRAY)
        self.cell(150, 5, "Augmented Reality (AR) - Master's Degree Presentation", ln=False)
        self.set_xy(250, 156)
        self.cell(31, 5, f"{slide_num} of 7", align="R")


def build_pdf():
    pdf = ARPresentationPDF()

    # ==========================================
    # SLIDE 1: TITLE SLIDE
    # ==========================================
    pdf.add_page()
    pdf.draw_background()

    img_title = os.path.join(IMAGES_DIR, "slide1_title.jpg")
    if os.path.exists(img_title):
        # Image on the right half
        pdf.image(img_title, x=155, y=18, w=128, h=130)

    # Left content card
    pdf.draw_card(16, 18, 132, 130, fill=CARD_BG)

    # Badge
    pdf.draw_card(26, 28, 48, 7, fill=BLUE, border=None, r=2)
    pdf.set_xy(26, 28)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(*WHITE)
    pdf.cell(48, 7, "MASTER'S PRESENTATION", align="C")

    # Main Title
    pdf.set_xy(26, 40)
    pdf.set_font("Helvetica", "B", 26)
    pdf.set_text_color(*CYAN)
    pdf.cell(112, 12, "AUGMENTED REALITY", ln=True)

    # Subtitle
    pdf.set_xy(26, 54)
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(*WHITE)
    pdf.multi_cell(112, 7, "Understanding the Technology and Its Real-World Applications")

    # Short description
    pdf.set_xy(26, 75)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*LIGHT_GRAY)
    desc = (
        "An educational overview of Augmented Reality:\n"
        "- What it is & how it enhances the physical world\n"
        "- Difference between AR and VR\n"
        "- Core technology pipeline & major application domains\n"
        "- Live marker-based WebAR demonstration"
    )
    pdf.multi_cell(112, 5.5, desc)

    # Presenter info
    pdf.draw_card(26, 112, 112, 24, fill=(12, 18, 48), border=CARD_BORDER)
    pdf.set_xy(30, 115)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*CYAN)
    pdf.cell(100, 5, "Presenter: Master's Degree Student", ln=True)
    pdf.set_xy(30, 121)
    pdf.set_font("Helvetica", "", 8.5)
    pdf.set_text_color(*LIGHT_GRAY)
    pdf.cell(100, 5, "Duration: 30 Minutes  |  Format: Educational & Visual", ln=True)
    pdf.set_xy(30, 127)
    pdf.cell(100, 5, "Audience: University Students & Faculty", ln=True)

    pdf.draw_footer(1)

    # ==========================================
    # SLIDE 2: WHAT IS AUGMENTED REALITY?
    # ==========================================
    pdf.add_page()
    pdf.draw_background()
    pdf.draw_header(2, "What is Augmented Reality?", "Simple definition, core concept, and everyday examples")

    img_s2 = os.path.join(IMAGES_DIR, "slide2_what_is_ar.jpg")
    if os.path.exists(img_s2):
        pdf.image(img_s2, x=165, y=38, w=118, h=112)

    # Left column: Concept Card + Examples
    pdf.draw_card(16, 38, 142, 34, fill=CARD_BG)
    pdf.set_xy(22, 42)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(*CYAN)
    pdf.cell(130, 6, "Core Definition", ln=True)
    pdf.set_xy(22, 49)
    pdf.set_font("Helvetica", "", 10.5)
    pdf.set_text_color(*WHITE)
    def_text = (
        "Augmented Reality (AR) adds digital elements - 3D models, graphics, sounds, or data - "
        "on top of the real physical world in real time."
    )
    pdf.multi_cell(130, 5.2, def_text)

    # 3 Real-World Examples
    examples = [
        ("Snapchat & Instagram Filters", "Face tracking detects your facial landmarks and attaches interactive digital masks, glasses, or effects.", CYAN),
        ("Pokemon GO & Mobile Games", "Camera sees the sidewalk or park; the app places digital creatures that appear to stand on the ground.", BLUE),
        ("IKEA Place & Furniture Preview", "Floor detection measures your room; preview 3D furniture at true 1:1 scale before purchasing.", GREEN),
    ]

    y_ex = 76
    for title_ex, desc_ex, col in examples:
        pdf.draw_card(16, y_ex, 142, 23, fill=CARD_BG)
        # Bullet marker
        pdf.draw_card(20, y_ex + 4, 3, 15, fill=col, border=None)
        pdf.set_xy(26, y_ex + 3)
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(*col)
        pdf.cell(128, 5, title_ex, ln=True)
        pdf.set_xy(26, y_ex + 9)
        pdf.set_font("Helvetica", "", 8.5)
        pdf.set_text_color(*LIGHT_GRAY)
        pdf.multi_cell(128, 4.2, desc_ex)
        y_ex += 25

    pdf.draw_footer(2)

    # ==========================================
    # SLIDE 3: AR VS VR
    # ==========================================
    pdf.add_page()
    pdf.draw_background()
    pdf.draw_header(3, "Augmented Reality vs Virtual Reality", "Key differences, immersion levels, and device requirements")

    img_s3 = os.path.join(IMAGES_DIR, "slide3_ar_vs_vr.jpg")
    if os.path.exists(img_s3):
        pdf.image(img_s3, x=16, y=38, w=110, h=112)

    # Right side: AR Card vs VR Card
    # AR Card
    pdf.draw_card(132, 38, 72, 112, fill=CARD_BG, border=CYAN)
    pdf.draw_card(138, 44, 60, 7, fill=CYAN, border=None, r=2)
    pdf.set_xy(138, 44)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*NAVY_BG)
    pdf.cell(60, 7, "AUGMENTED REALITY (AR)", align="C")

    ar_points = [
        ("Environment", "Real world + digital overlay"),
        ("Immersion", "Partially immersed (see reality)"),
        ("Devices", "Smartphones, tablets, smart glasses"),
        ("Field of View", "Open, transparent to surroundings"),
        ("User State", "Aware and connected to room"),
        ("Core Mantra", "\"Adds digital info to reality\"")
    ]
    y_p = 56
    for label, val in ar_points:
        pdf.set_xy(136, y_p)
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_text_color(*CYAN)
        pdf.cell(64, 4, label, ln=True)
        pdf.set_xy(136, y_p + 4)
        pdf.set_font("Helvetica", "", 8.5)
        pdf.set_text_color(*WHITE)
        pdf.multi_cell(64, 4, val)
        y_p += 14.5

    # VR Card
    pdf.draw_card(209, 38, 72, 112, fill=CARD_BG, border=PURPLE)
    pdf.draw_card(215, 44, 60, 7, fill=PURPLE, border=None, r=2)
    pdf.set_xy(215, 44)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*WHITE)
    pdf.cell(60, 7, "VIRTUAL REALITY (VR)", align="C")

    vr_points = [
        ("Environment", "100% synthetic computer world"),
        ("Immersion", "Fully immersed (shut out reality)"),
        ("Devices", "Opaque headsets (Meta Quest, etc.)"),
        ("Field of View", "Enclosed, sensory isolation"),
        ("User State", "Inside a simulated environment"),
        ("Core Mantra", "\"Completely replaces reality\"")
    ]
    y_p = 56
    for label, val in vr_points:
        pdf.set_xy(213, y_p)
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_text_color(*PURPLE)
        pdf.cell(64, 4, label, ln=True)
        pdf.set_xy(213, y_p + 4)
        pdf.set_font("Helvetica", "", 8.5)
        pdf.set_text_color(*WHITE)
        pdf.multi_cell(64, 4, val)
        y_p += 14.5

    pdf.draw_footer(3)

    # ==========================================
    # SLIDE 4: HOW AR WORKS
    # ==========================================
    pdf.add_page()
    pdf.draw_background()
    pdf.draw_header(4, "How Augmented Reality Works", "The 4-step real-time processing pipeline explained simply")

    steps = [
        ("1. CAMERA CAPTURE", "Sensors & Video Feed", "The device camera continuously streams high-framerate video frames of the surrounding physical environment.", CYAN),
        ("2. SCENE DETECTION", "Surfaces & Markers", "Computer vision algorithms detect flat surfaces (floors, tables), feature points, or predefined visual markers.", BLUE),
        ("3. 3D RENDERING", "Position & Scale", "The rendering engine computes exact perspective, depth, scale, and lighting for 3D virtual objects.", PURPLE),
        ("4. SCREEN DISPLAY", "Real-time Fusion", "The real camera image and digital elements are merged at 60 FPS on screen so objects look anchored in place.", GREEN)
    ]

    card_w = 62
    gap = 7
    start_x = 16
    for i, (stitle, ssub, sbody, scol) in enumerate(steps):
        x = start_x + i * (card_w + gap)
        pdf.draw_card(x, 38, card_w, 82, fill=CARD_BG, border=scol)

        # Step indicator
        pdf.draw_card(x + 5, 43, 20, 6, fill=scol, border=None, r=2)
        pdf.set_xy(x + 5, 43)
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_text_color(*(NAVY_BG if scol == CYAN else WHITE))
        pdf.cell(20, 6, f"STEP {i+1}", align="C")

        # Title
        pdf.set_xy(x + 5, 52)
        pdf.set_font("Helvetica", "B", 9.5)
        pdf.set_text_color(*scol)
        pdf.multi_cell(card_w - 10, 4.5, stitle)

        # Subtitle
        pdf.set_xy(x + 5, 62)
        pdf.set_font("Helvetica", "B", 8.5)
        pdf.set_text_color(*WHITE)
        pdf.cell(card_w - 10, 4, ssub, ln=True)

        # Description
        pdf.set_xy(x + 5, 68)
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(*LIGHT_GRAY)
        pdf.multi_cell(card_w - 10, 4.2, sbody)

    # Bottom summary card
    pdf.draw_card(16, 124, 265, 26, fill=(15, 24, 55), border=CARD_BORDER)
    pdf.set_xy(22, 127)
    pdf.set_font("Helvetica", "B", 9.5)
    pdf.set_text_color(*CYAN)
    pdf.cell(250, 5, "Key Takeaway for Students:", ln=True)
    pdf.set_xy(22, 134)
    pdf.set_font("Helvetica", "", 8.5)
    pdf.set_text_color(*WHITE)
    summary_text = (
        "All 4 steps happen in milliseconds! Every time you move your device, the camera tracks your movement "
        "and updates the 3D position instantly. This gives the illusion that virtual objects are physically solid and real."
    )
    pdf.multi_cell(250, 4.5, summary_text)

    pdf.draw_footer(4)

    # ==========================================
    # SLIDE 5: TYPES & APPLICATIONS
    # ==========================================
    pdf.add_page()
    pdf.draw_background()
    pdf.draw_header(5, "Types & Real-World Applications of AR", "Four primary technical classifications and where they solve real problems")

    # Left: 4 Types
    pdf.draw_card(16, 38, 126, 112, fill=CARD_BG)
    pdf.set_xy(22, 42)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*CYAN)
    pdf.cell(115, 6, "Four Types of Augmented Reality", ln=True)

    types = [
        ("1. Marker-Based AR", "Uses a physical printed pattern (like a QR or Hiro marker). The camera calculates camera distance and angle from the known visual shape.", CYAN),
        ("2. Markerless AR (SLAM)", "Uses phone sensors (gyroscope, accelerometer) and camera to map unknown rooms and surfaces without any marker (IKEA Place, ARKit).", BLUE),
        ("3. Projection-Based AR", "Projects synthetic light onto physical surfaces. Users interact with light directly without holding a screen (virtual touch keyboards).", GREEN),
        ("4. Superimposition AR", "Replaces or supplements part of an object with an augmented view (e.g., overlaying an anatomical X-ray directly onto a patient's limb).", AMBER)
    ]
    y_t = 50
    for t_name, t_desc, t_col in types:
        pdf.draw_card(20, y_t, 118, 22, fill=(12, 18, 48), border=CARD_BORDER)
        pdf.set_xy(24, y_t + 2)
        pdf.set_font("Helvetica", "B", 8.5)
        pdf.set_text_color(*t_col)
        pdf.cell(110, 4.5, t_name, ln=True)
        pdf.set_xy(24, y_t + 7)
        pdf.set_font("Helvetica", "", 7.5)
        pdf.set_text_color(*LIGHT_GRAY)
        pdf.multi_cell(110, 3.6, t_desc)
        y_t += 24

    # Right: 4 Sectors / Applications
    pdf.draw_card(148, 38, 133, 112, fill=CARD_BG)
    pdf.set_xy(154, 42)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*WHITE)
    pdf.cell(120, 6, "Key Real-World Application Sectors", ln=True)

    apps = [
        ("Healthcare & Surgery", "Surgeons view 3D organ scans overlaid on patients during operations, minimizing incisions and improving precision.", CYAN),
        ("Education & Training", "Students explore 3D human anatomy, chemical reactions, or space science interactively instead of reading flat textbooks.", BLUE),
        ("Retail & E-Commerce", "Virtual 'try-on' for eyewear, makeup, and shoes; previewing furniture in real rooms before buying, cutting return rates.", GREEN),
        ("Industrial Maintenance", "Engineers wear smart glasses displaying step-by-step repair guides and wiring diagrams floating above real equipment.", AMBER)
    ]
    y_a = 50
    for a_name, a_desc, a_col in apps:
        pdf.draw_card(152, y_a, 125, 22, fill=(12, 18, 48), border=CARD_BORDER)
        pdf.set_xy(156, y_a + 2)
        pdf.set_font("Helvetica", "B", 8.5)
        pdf.set_text_color(*a_col)
        pdf.cell(118, 4.5, a_name, ln=True)
        pdf.set_xy(156, y_a + 7)
        pdf.set_font("Helvetica", "", 7.5)
        pdf.set_text_color(*LIGHT_GRAY)
        pdf.multi_cell(118, 3.6, a_desc)
        y_a += 24

    pdf.draw_footer(5)

    # ==========================================
    # SLIDE 6: ADVANTAGES & LIMITATIONS
    # ==========================================
    pdf.add_page()
    pdf.draw_background()
    pdf.draw_header(6, "Advantages & Current Limitations", "A balanced assessment of Augmented Reality's strengths and technical hurdles")

    # Left: Advantages
    pdf.draw_card(16, 38, 130, 112, fill=CARD_BG, border=GREEN)
    pdf.draw_card(22, 44, 45, 7, fill=GREEN, border=None, r=2)
    pdf.set_xy(22, 44)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*NAVY_BG)
    pdf.cell(45, 7, "ADVANTAGES", align="C")

    advantages = [
        ("Highly Engaging & Interactive", "Boosts memory retention and engagement in education by allowing students to touch and inspect 3D models."),
        ("No Complete Isolation", "Users stay aware of their real surroundings, avoiding motion sickness and safety risks common in VR."),
        ("Accessible via Mobile Phones", "Hundreds of millions of standard smartphones can run AR experiences immediately without expensive headsets."),
        ("Hands-Free Efficiency", "With AR smart glasses, technicians and doctors receive vital instructions without taking their hands off their work."),
        ("Improved Decision-Making", "Visualizing products or architectural blueprints in context reduces planning errors and purchase returns.")
    ]
    y_adv = 55
    for atitle, abody in advantages:
        pdf.set_xy(22, y_adv)
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_text_color(*GREEN)
        pdf.cell(118, 4, "+  " + atitle, ln=True)
        pdf.set_xy(26, y_adv + 4)
        pdf.set_font("Helvetica", "", 7.5)
        pdf.set_text_color(*LIGHT_GRAY)
        pdf.multi_cell(118, 3.5, abody)
        y_adv += 17

    # Right: Limitations
    pdf.draw_card(151, 38, 130, 112, fill=CARD_BG, border=AMBER)
    pdf.draw_card(157, 44, 45, 7, fill=AMBER, border=None, r=2)
    pdf.set_xy(157, 44)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*NAVY_BG)
    pdf.cell(45, 7, "LIMITATIONS", align="C")

    limitations = [
        ("Battery & Processing Drain", "Continuous camera streaming, computer vision, and 3D rendering cause mobile devices to heat up and drain battery quickly."),
        ("Sensitivity to Lighting", "Marker and surface tracking degrade severely in low light, direct sunlight glare, or on textureless white walls."),
        ("Privacy & Security Issues", "Cameras constantly recording physical environments raise serious privacy concerns in homes and public spaces."),
        ("Hardware Cost & Bulk", "High-performance AR glasses (like Microsoft HoloLens or Apple Vision Pro) remain expensive and heavy for all-day wear."),
        ("Narrow Field of View", "Many existing AR glasses project digital graphics into a limited rectangular box rather than your full natural eyesight.")
    ]
    y_lim = 55
    for ltitle, lbody in limitations:
        pdf.set_xy(157, y_lim)
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_text_color(*AMBER)
        pdf.cell(118, 4, "-  " + ltitle, ln=True)
        pdf.set_xy(161, y_lim + 4)
        pdf.set_font("Helvetica", "", 7.5)
        pdf.set_text_color(*LIGHT_GRAY)
        pdf.multi_cell(118, 3.5, lbody)
        y_lim += 17

    pdf.draw_footer(6)

    # ==========================================
    # SLIDE 7: PRACTICAL DEMO & CONCLUSION
    # ==========================================
    pdf.add_page()
    pdf.draw_background()
    pdf.draw_header(7, "Practical Demonstration & Key Takeaways", "Live WebAR marker demonstration and recap of core concepts")

    # Left: Practical Demo Box
    pdf.draw_card(16, 38, 130, 112, fill=CARD_BG, border=CYAN)
    pdf.set_xy(22, 42)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*CYAN)
    pdf.cell(118, 6, "Live Practical Demonstration", ln=True)

    marker_img = os.path.join(PROJECT_DIR, "demo", "marker.png")
    if os.path.exists(marker_img):
        pdf.image(marker_img, x=22, y=52, w=34, h=34)

    pdf.set_xy(60, 52)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*WHITE)
    pdf.cell(80, 5, "AR Solar System Experience", ln=True)
    pdf.set_xy(60, 58)
    pdf.set_font("Helvetica", "", 7.5)
    pdf.set_text_color(*LIGHT_GRAY)
    demo_bullets = (
        "- Technology: WebAR (AR.js + A-Frame)\n"
        "- Works directly in mobile browser\n"
        "- No app installation required\n"
        "- Uses standard printed Hiro marker\n"
        "- Demonstrates marker-based tracking"
    )
    pdf.multi_cell(80, 3.8, demo_bullets)

    # How it demonstrates the concepts
    pdf.draw_card(22, 90, 118, 52, fill=(12, 18, 48), border=CARD_BORDER)
    pdf.set_xy(26, 93)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(*GREEN)
    pdf.cell(110, 4.5, "Live Concept Demonstration Steps:", ln=True)
    pdf.set_xy(26, 99)
    pdf.set_font("Helvetica", "", 7.5)
    pdf.set_text_color(*LIGHT_GRAY)
    steps_demo = (
        "1. Camera captures the printed Hiro marker on the desk\n"
        "2. Computer vision detects the black square & calculates 3D pose\n"
        "3. Sun and orbiting planets appear anchored in real 3D space\n"
        "4. Move phone around marker: perspective and angles adjust naturally\n"
        "-> Demonstrates Camera -> Detection -> 3D Render -> Display in real time!"
    )
    pdf.multi_cell(110, 3.8, steps_demo)

    # Right: Key Takeaways & Q&A
    pdf.draw_card(151, 38, 130, 80, fill=CARD_BG)
    pdf.set_xy(157, 42)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*CYAN)
    pdf.cell(118, 6, "5 Key Takeaways to Remember", ln=True)

    takeaways = [
        "1. AR enhances reality by adding digital 3D content, while VR replaces reality.",
        "2. Core pipeline: Camera Capture -> Scene Detection -> 3D Render -> Display.",
        "3. Four types: Marker-based, Markerless (SLAM), Projection, and Superimposition.",
        "4. Powerful applications across medicine, education, retail, and engineering.",
        "5. Accessible today via standard smartphones, evolving toward smart glasses."
    ]
    y_tk = 50
    for tk in takeaways:
        pdf.set_xy(157, y_tk)
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(*WHITE)
        pdf.multi_cell(118, 4, tk)
        y_tk += 9.5

    # Thank you & Q&A Box
    pdf.draw_card(151, 122, 130, 28, fill=(15, 24, 60), border=CYAN)
    pdf.set_xy(157, 125)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(*CYAN)
    pdf.cell(118, 6, "Thank You for Your Attention!", align="C")
    pdf.set_xy(157, 133)
    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_text_color(*WHITE)
    pdf.cell(118, 5, "I welcome any questions or discussion points.", align="C")
    pdf.set_xy(157, 139)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*LIGHT_GRAY)
    pdf.cell(118, 5, "Q&A Session", align="C")

    pdf.draw_footer(7)

    # Save PDF
    pdf.output(OUTPUT_PDF)
    print(f"Presentation PDF successfully created at: {OUTPUT_PDF}")


if __name__ == "__main__":
    build_pdf()
