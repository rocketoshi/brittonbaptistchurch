#!/usr/bin/env python3
"""
Comprehensive BBC site update:
1. Full 11-page nav on every page
2. Full-width hero images
3. Link all facility pages from ministries and homepage
4. Fix any remaining issues
Run from ~/brittonbaptistchurch/
"""
import glob
import re

# ── New navigation HTML ──────────────────────────────────────────────────

def make_nav(active=""):
    pages = [
        ("home", "/", "Home"),
        ("about", "/about.html", "About"),
        ("sanctuary", "/sanctuary.html", "Sanctuary"),
        ("ministries", "/ministries.html", "Ministries"),
        ("daycare", "/daycare.html", "Daycare"),
        ("sewing", "/sewing-club.html", "Sewing Club"),
        ("food", "/food-pantry.html", "Food Pantry"),
        ("court", "/court-rental.html", "Court Rental"),
        ("contact", "/contact.html", "Contact"),
    ]
    items = ""
    for key, href, label in pages:
        style = ' style="color:var(--gold);"' if key == active else ''
        items += f'        <li><a href="{href}"{style}>{label}</a></li>\n'
    items += '        <li><a href="/court-rental.html#booking" class="nav-cta">Book a Court</a></li>\n'
    return items

# Map filename to active key
file_active = {
    "index.html": "home",
    "about.html": "about",
    "sanctuary.html": "sanctuary",
    "chapel.html": "sanctuary",  # sub-page of sanctuary
    "ministries.html": "ministries",
    "daycare.html": "daycare",
    "sewing-club.html": "sewing",
    "food-pantry.html": "food",
    "fellowship-hall.html": "ministries",
    "court-rental.html": "court",
    "contact.html": "contact",
}

# ── Update nav on all pages ──────────────────────────────────────────────

for filename in glob.glob("*.html"):
    with open(filename, 'r') as f:
        content = f.read()
    
    if '<ul class="nav-menu" id="navMenu">' not in content:
        continue
    
    # Extract and replace the nav items
    nav_start = content.find('<ul class="nav-menu" id="navMenu">') + len('<ul class="nav-menu" id="navMenu">\n')
    nav_end = content.find('      </ul>', nav_start)
    
    active = file_active.get(filename, "")
    new_items = make_nav(active)
    
    content = content[:nav_start] + new_items + content[nav_end:]
    
    with open(filename, 'w') as f:
        f.write(content)
    
    # Count new items
    count = new_items.count('<li>')
    print(f"  {filename}: nav updated ({count} items, active={active})")

print()

# ── Add full-width hero images where missing ─────────────────────────────

# Homepage: make hero image truly full-width background
with open('index.html', 'r') as f:
    c = f.read()

# Fix hero to use exterior image as full background
if 'url(/images/exterior-01.jpg)' not in c:
    c = c.replace(
        '<section class="hero">',
        '<section class="hero" style="background-image:linear-gradient(rgba(15,31,61,0.85),rgba(15,31,61,0.88)),url(/images/exterior-01.jpg);background-size:cover;background-position:center;">'
    )
    print("  index.html: hero background image added")

# Add full-width exterior photo strip after hero
if 'full-width-exterior' not in c:
    hero_end = c.find('<!-- Preview Cards -->')
    if hero_end > 0:
        exterior_strip = """
  <!-- Full-width exterior photo -->
  <div id="full-width-exterior" style="width:100%;height:350px;overflow:hidden;">
    <img src="/images/exterior-04-wide.jpg" alt="Britton Baptist Church building exterior Oklahoma City" style="width:100%;height:100%;object-fit:cover;" loading="lazy">
  </div>

"""
        c = c[:hero_end] + exterior_strip + c[hero_end:]
        print("  index.html: full-width exterior strip added")

with open('index.html', 'w') as f:
    f.write(c)

# Court rental: add full-width gym photo
with open('court-rental.html', 'r') as f:
    c = f.read()

# Add full-width gym panoramic after hero
if 'full-width-gym' not in c:
    features_start = c.find('<!-- Features -->')
    if features_start > 0:
        gym_strip = """
  <!-- Full-width gym photo -->
  <div id="full-width-gym" style="width:100%;height:400px;overflow:hidden;">
    <img src="/images/gym-02-panoramic.jpg" alt="Indoor Basketball Court at Britton Baptist Church Oklahoma City" style="width:100%;height:100%;object-fit:cover;" loading="lazy">
  </div>

"""
        c = c[:features_start] + gym_strip + c[features_start:]
        print("  court-rental.html: full-width gym strip added")

with open('court-rental.html', 'w') as f:
    f.write(c)

# Sanctuary: add full-width sanctuary photo
with open('sanctuary.html', 'r') as f:
    c = f.read()

if 'full-width-sanctuary' not in c:
    sect_start = c.find('<section class="sect" style="background:var(--cream);">')
    if sect_start > 0:
        sanc_strip = """
  <!-- Full-width sanctuary photo -->
  <div id="full-width-sanctuary" style="width:100%;height:400px;overflow:hidden;">
    <img src="/images/sanctuary-01.jpg" alt="Britton Baptist Church Sanctuary Interior" style="width:100%;height:100%;object-fit:cover;" loading="lazy">
  </div>

"""
        c = c[:sect_start] + sanc_strip + c[sect_start:]
        print("  sanctuary.html: full-width sanctuary strip added")

with open('sanctuary.html', 'w') as f:
    f.write(c)

# Daycare: add full-width daycare photo
with open('daycare.html', 'r') as f:
    c = f.read()

if 'full-width-daycare' not in c:
    sect_start = c.find('<section class="sect" style="background:var(--cream);">')
    if sect_start > 0:
        dc_strip = """
  <!-- Full-width daycare photo -->
  <div id="full-width-daycare" style="width:100%;height:350px;overflow:hidden;">
    <img src="/images/daycare-01.jpg" alt="Nursery and Daycare at Britton Baptist Church Oklahoma City" style="width:100%;height:100%;object-fit:cover;" loading="lazy">
  </div>

"""
        c = c[:sect_start] + dc_strip + c[sect_start:]
        print("  daycare.html: full-width daycare strip added")

with open('daycare.html', 'w') as f:
    f.write(c)

# Sewing club: add full-width sewing photo
with open('sewing-club.html', 'r') as f:
    c = f.read()

if 'full-width-sewing' not in c:
    sect_start = c.find('<section class="sect" style="background:var(--cream);">')
    if sect_start > 0:
        sew_strip = """
  <!-- Full-width sewing photo -->
  <div id="full-width-sewing" style="width:100%;height:350px;overflow:hidden;">
    <img src="/images/sewing-02.jpg" alt="Sewing and Quilting Ministry at Britton Baptist Church" style="width:100%;height:100%;object-fit:cover;" loading="lazy">
  </div>

"""
        c = c[:sect_start] + sew_strip + c[sect_start:]
        print("  sewing-club.html: full-width sewing strip added")

with open('sewing-club.html', 'w') as f:
    f.write(c)

# Food pantry: add full-width photo
with open('food-pantry.html', 'r') as f:
    c = f.read()

if 'full-width-pantry' not in c:
    sect_start = c.find('<section class="sect" style="background:var(--cream);">')
    if sect_start > 0:
        fp_strip = """
  <!-- Full-width food pantry photo -->
  <div id="full-width-pantry" style="width:100%;height:350px;overflow:hidden;">
    <img src="/images/food-pantry-01.jpg" alt="Food Pantry at Britton Baptist Church Oklahoma City" style="width:100%;height:100%;object-fit:cover;" loading="lazy">
  </div>

"""
        c = c[:sect_start] + fp_strip + c[sect_start:]
        print("  food-pantry.html: full-width pantry strip added")

with open('food-pantry.html', 'w') as f:
    f.write(c)

# Fellowship hall: add full-width photo
with open('fellowship-hall.html', 'r') as f:
    c = f.read()

if 'full-width-fellowship' not in c:
    sect_start = c.find('<section class="sect" style="background:var(--cream);">')
    if sect_start > 0:
        fh_strip = """
  <!-- Full-width fellowship hall photo -->
  <div id="full-width-fellowship" style="width:100%;height:350px;overflow:hidden;">
    <img src="/images/cafeteria-01.jpg" alt="Fellowship Hall at Britton Baptist Church Oklahoma City" style="width:100%;height:100%;object-fit:cover;" loading="lazy">
  </div>

"""
        c = c[:sect_start] + fh_strip + c[sect_start:]
        print("  fellowship-hall.html: full-width fellowship strip added")

with open('fellowship-hall.html', 'w') as f:
    f.write(c)

# About: add full-width sanctuary photo
with open('about.html', 'r') as f:
    c = f.read()

if 'full-width-about' not in c:
    sect_start = c.find('<section class="sect" style="background:var(--cream);">')
    if sect_start > 0:
        about_strip = """
  <!-- Full-width sanctuary photo -->
  <div id="full-width-about" style="width:100%;height:350px;overflow:hidden;">
    <img src="/images/sanctuary-05.jpg" alt="Inside Britton Baptist Church Oklahoma City" style="width:100%;height:100%;object-fit:cover;" loading="lazy">
  </div>

"""
        c = c[:sect_start] + about_strip + c[sect_start:]
        print("  about.html: full-width interior strip added")

with open('about.html', 'w') as f:
    f.write(c)

# Contact: add full-width exterior photo  
with open('contact.html', 'r') as f:
    c = f.read()

if 'full-width-contact' not in c:
    sect_start = c.find('<section class="sect" style="background:var(--cream);">')
    if sect_start > 0:
        contact_strip = """
  <!-- Full-width exterior photo -->
  <div id="full-width-contact" style="width:100%;height:350px;overflow:hidden;">
    <img src="/images/exterior-03.jpg" alt="Britton Baptist Church Building Oklahoma City" style="width:100%;height:100%;object-fit:cover;" loading="lazy">
  </div>

"""
        c = c[:sect_start] + contact_strip + c[sect_start:]
        print("  contact.html: full-width exterior strip added")

with open('contact.html', 'w') as f:
    f.write(c)

# Ministries: add full-width photo and link facility cards
with open('ministries.html', 'r') as f:
    c = f.read()

if 'full-width-ministries' not in c:
    # Find the "Our Facilities" section
    facilities_start = c.find('<!-- Our Facilities -->')
    if facilities_start > 0:
        min_strip = """
  <!-- Full-width hallway photo -->
  <div id="full-width-ministries" style="width:100%;height:300px;overflow:hidden;">
    <img src="/images/hallway-01.jpg" alt="Inside Britton Baptist Church hallway" style="width:100%;height:100%;object-fit:cover;" loading="lazy">
  </div>

"""
        c = c[:facilities_start] + min_strip + c[facilities_start:]
        print("  ministries.html: full-width hallway strip added")

with open('ministries.html', 'w') as f:
    f.write(c)

# Chapel: add full-width photo
with open('chapel.html', 'r') as f:
    c = f.read()

if 'full-width-chapel' not in c:
    sect_start = c.find('<section class="sect" style="background:var(--cream);">')
    if sect_start > 0:
        ch_strip = """
  <!-- Full-width chapel photo -->
  <div id="full-width-chapel" style="width:100%;height:350px;overflow:hidden;">
    <img src="/images/chapel-01.jpg" alt="Chapel at Britton Baptist Church Oklahoma City" style="width:100%;height:100%;object-fit:cover;" loading="lazy">
  </div>

"""
        c = c[:sect_start] + ch_strip + c[sect_start:]
        print("  chapel.html: full-width chapel strip added")

with open('chapel.html', 'w') as f:
    f.write(c)

# ── Add hallway photos to about page ─────────────────────────────────────

with open('about.html', 'r') as f:
    c = f.read()

# Add hallway gallery after the campus photos
if 'hallway-01' not in c:
    campus_end = c.find('</div>\n        </div>\n\n        <div class="abc-plan">')
    if campus_end > 0:
        hallway_gallery = """
          <!-- Hallway & Interior Photos -->
          <div style="margin-top:20px;">
            <h4 style="font-family:'Nunito Sans',sans-serif;font-size:0.95rem;font-weight:600;color:var(--navy);margin-bottom:10px;">Around Our Campus</h4>
            <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px;">
              <img src="/images/hallway-01.jpg" alt="Britton Baptist Church interior hallway" style="border-radius:6px;width:100%;height:100px;object-fit:cover;" loading="lazy">
              <img src="/images/hallway-04.jpg" alt="Britton Baptist Church lobby" style="border-radius:6px;width:100%;height:100px;object-fit:cover;" loading="lazy">
              <img src="/images/hallway-06.jpg" alt="Inside Britton Baptist Church" style="border-radius:6px;width:100%;height:100px;object-fit:cover;" loading="lazy">
            </div>
          </div>
"""
        c = c[:campus_end] + hallway_gallery + c[campus_end:]
        print("  about.html: hallway gallery added")
        with open('about.html', 'w') as f:
            f.write(c)

print("\nAll updates complete!")
