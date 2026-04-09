#!/usr/bin/env python3
"""
Add real photos to all BBC pages.
Run from ~/brittonbaptistchurch/
"""

# ── Helper: photo gallery component ──────────────────────────────────────

def photo_grid(photos, style=""):
    """photos = list of (src, alt) tuples"""
    items = ""
    for src, alt in photos:
        items += f'        <img src="/images/{src}" alt="{alt}" style="border-radius:10px;object-fit:cover;width:100%;height:220px;" loading="lazy">\n'
    cols = min(len(photos), 3)
    return f"""    <div style="display:grid;grid-template-columns:repeat({cols},1fr);gap:12px;margin-top:24px;{style}">
{items}    </div>"""

# ══════════════════════════════════════════════════════════════════════════
# INDEX.HTML — Add exterior photo to hero, facility preview photos
# ══════════════════════════════════════════════════════════════════════════

with open('index.html', 'r') as f:
    c = f.read()

# Add hero background image
c = c.replace(
    '<section class="hero">',
    '<section class="hero" style="background-image:linear-gradient(rgba(15,31,61,0.88),rgba(15,31,61,0.92)),url(/images/exterior-front.jpg);background-size:cover;background-position:center;">'
)

# Add facility photos to the preview cards section - after the 3 cards grid closes
old_cards_end = """      </div>
    </div>
  </section>

  <!-- Court Teaser -->"""

new_cards_end = """      </div>

      <!-- Our Facilities -->
      <div style="margin-top:56px;">
        <h3 style="font-family:'Cormorant Garamond',serif;font-size:1.6rem;color:var(--navy);text-align:center;margin-bottom:8px;">Our Facilities</h3>
        <p style="text-align:center;color:var(--text-soft);font-size:0.9rem;margin-bottom:24px;">A campus built for worship, community, and fellowship.</p>
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;">
          <div style="position:relative;border-radius:10px;overflow:hidden;">
            <img src="/images/sanctuary-main.jpg" alt="Britton Baptist Church Sanctuary" style="width:100%;height:200px;object-fit:cover;display:block;" loading="lazy">
            <div style="position:absolute;bottom:0;left:0;right:0;padding:10px 12px;background:linear-gradient(transparent,rgba(0,0,0,0.7));"><span style="color:white;font-size:0.78rem;font-weight:600;">Sanctuary</span></div>
          </div>
          <div style="position:relative;border-radius:10px;overflow:hidden;">
            <img src="/images/gym-panoramic.jpg" alt="Basketball Court at Britton Baptist Church" style="width:100%;height:200px;object-fit:cover;display:block;" loading="lazy">
            <div style="position:absolute;bottom:0;left:0;right:0;padding:10px 12px;background:linear-gradient(transparent,rgba(0,0,0,0.7));"><span style="color:white;font-size:0.78rem;font-weight:600;">Basketball Court</span></div>
          </div>
          <div style="position:relative;border-radius:10px;overflow:hidden;">
            <img src="/images/cafeteria.jpg" alt="Fellowship Hall at Britton Baptist Church" style="width:100%;height:200px;object-fit:cover;display:block;" loading="lazy">
            <div style="position:absolute;bottom:0;left:0;right:0;padding:10px 12px;background:linear-gradient(transparent,rgba(0,0,0,0.7));"><span style="color:white;font-size:0.78rem;font-weight:600;">Fellowship Hall</span></div>
          </div>
          <div style="position:relative;border-radius:10px;overflow:hidden;">
            <img src="/images/daycare-room.jpg" alt="Nursery and Daycare at Britton Baptist Church" style="width:100%;height:200px;object-fit:cover;display:block;" loading="lazy">
            <div style="position:absolute;bottom:0;left:0;right:0;padding:10px 12px;background:linear-gradient(transparent,rgba(0,0,0,0.7));"><span style="color:white;font-size:0.78rem;font-weight:600;">Nursery &amp; Daycare</span></div>
          </div>
        </div>
      </div>

    </div>
  </section>

  <!-- Court Teaser -->"""

c = c.replace(old_cards_end, new_cards_end)

with open('index.html', 'w') as f:
    f.write(c)
print("index.html updated with photos")


# ══════════════════════════════════════════════════════════════════════════
# ABOUT.HTML — Add sanctuary photos, exterior, chapel
# ══════════════════════════════════════════════════════════════════════════

with open('about.html', 'r') as f:
    c = f.read()

# Add exterior photo as hero background
c = c.replace(
    '<section style="padding:120px 24px 60px;background:var(--deep-blue);text-align:center;">',
    '<section style="padding:120px 24px 60px;background-image:linear-gradient(rgba(15,31,61,0.85),rgba(15,31,61,0.9)),url(/images/exterior-wide.jpg);background-size:cover;background-position:center;text-align:center;">',
    1  # only first occurrence
)

# Add photos after the mission text, before the ABC plan
old_about = """          <p style="font-size:0.95rem;color:var(--text-soft);line-height:1.8;">Our doors are open to everyone. Come as you are and discover what it means to walk in the light together.</p>
        </div>

        <div class="abc-plan">"""

new_about = """          <p style="font-size:0.95rem;color:var(--text-soft);line-height:1.8;">Our doors are open to everyone. Come as you are and discover what it means to walk in the light together.</p>

          <!-- Facility Photos -->
          <div style="margin-top:32px;">
            <h3 style="font-family:'Cormorant Garamond',serif;font-size:1.3rem;color:var(--navy);margin-bottom:16px;">Our Campus</h3>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
              <img src="/images/exterior-front.jpg" alt="Britton Baptist Church building" style="border-radius:8px;width:100%;height:160px;object-fit:cover;" loading="lazy">
              <img src="/images/sanctuary-main.jpg" alt="Britton Baptist Church sanctuary" style="border-radius:8px;width:100%;height:160px;object-fit:cover;" loading="lazy">
              <img src="/images/chapel-small.jpg" alt="Britton Baptist Church chapel" style="border-radius:8px;width:100%;height:160px;object-fit:cover;" loading="lazy">
              <img src="/images/exterior-sign.jpg" alt="Britton Baptist Church sign" style="border-radius:8px;width:100%;height:160px;object-fit:cover;" loading="lazy">
            </div>
          </div>
        </div>

        <div class="abc-plan">"""

c = c.replace(old_about, new_about)

with open('about.html', 'w') as f:
    f.write(c)
print("about.html updated with photos")


# ══════════════════════════════════════════════════════════════════════════
# MINISTRIES.HTML — Add photos to each ministry section
# ══════════════════════════════════════════════════════════════════════════

with open('ministries.html', 'r') as f:
    c = f.read()

# Add hero background
c = c.replace(
    '<section style="padding:120px 24px 60px;background:var(--deep-blue);text-align:center;">',
    '<section style="padding:120px 24px 60px;background-image:linear-gradient(rgba(15,31,61,0.85),rgba(15,31,61,0.9)),url(/images/sanctuary-pews.jpg);background-size:cover;background-position:center;text-align:center;">',
    1
)

# Add facilities section before the court teaser
old_court_teaser = """  <!-- Court Teaser -->
  <section class="sect" style="background:var(--cream);">"""

new_facilities = """  <!-- Our Facilities -->
  <section class="sect" style="background:var(--warm-white);">
    <div class="sect-inner">
      <div class="label">Our Facilities</div>
      <h2 class="sect-title">More Than Just a Church Building</h2>
      <p class="sect-sub">Our campus serves the community with a wide range of facilities and programs.</p>

      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:40px;">

        <div style="background:white;border-radius:12px;overflow:hidden;border:1px solid rgba(0,0,0,0.05);">
          <img src="/images/daycare-room.jpg" alt="Nursery and Daycare at Britton Baptist Church Oklahoma City" style="width:100%;height:180px;object-fit:cover;" loading="lazy">
          <div style="padding:20px;">
            <h4 style="font-family:'Nunito Sans',sans-serif;font-size:1rem;font-weight:700;color:var(--navy);margin-bottom:6px;">Nursery &amp; Daycare</h4>
            <p style="font-size:0.85rem;color:var(--text-soft);line-height:1.55;">Multiple rooms for infants and toddlers with dedicated caregivers. Safe, loving environment for your little ones during services and events.</p>
          </div>
        </div>

        <div style="background:white;border-radius:12px;overflow:hidden;border:1px solid rgba(0,0,0,0.05);">
          <img src="/images/sewing-room.jpg" alt="Sewing and Quilting Club at Britton Baptist Church" style="width:100%;height:180px;object-fit:cover;" loading="lazy">
          <div style="padding:20px;">
            <h4 style="font-family:'Nunito Sans',sans-serif;font-size:1rem;font-weight:700;color:var(--navy);margin-bottom:6px;">Sewing &amp; Quilting Club</h4>
            <p style="font-size:0.85rem;color:var(--text-soft);line-height:1.55;">Active sewing and knitting ministry with dedicated rooms, sewing machines, and regular meetups. Creating quilts and crafts for the community.</p>
          </div>
        </div>

        <div style="background:white;border-radius:12px;overflow:hidden;border:1px solid rgba(0,0,0,0.05);">
          <img src="/images/food-pantry.jpg" alt="Food Pantry at Britton Baptist Church Oklahoma City" style="width:100%;height:180px;object-fit:cover;" loading="lazy">
          <div style="padding:20px;">
            <h4 style="font-family:'Nunito Sans',sans-serif;font-size:1rem;font-weight:700;color:var(--navy);margin-bottom:6px;">Food Pantry</h4>
            <p style="font-size:0.85rem;color:var(--text-soft);line-height:1.55;">Stocked food pantry serving families in need across North Oklahoma City. Open to the community — no membership required.</p>
          </div>
        </div>

        <div style="background:white;border-radius:12px;overflow:hidden;border:1px solid rgba(0,0,0,0.05);">
          <img src="/images/cafeteria.jpg" alt="Fellowship Hall and Cafeteria at Britton Baptist Church" style="width:100%;height:180px;object-fit:cover;" loading="lazy">
          <div style="padding:20px;">
            <h4 style="font-family:'Nunito Sans',sans-serif;font-size:1rem;font-weight:700;color:var(--navy);margin-bottom:6px;">Fellowship Hall &amp; Kitchen</h4>
            <p style="font-size:0.85rem;color:var(--text-soft);line-height:1.55;">Large cafeteria with commercial kitchen. Wednesday fellowship meals, church dinners, and community events.</p>
          </div>
        </div>

        <div style="background:white;border-radius:12px;overflow:hidden;border:1px solid rgba(0,0,0,0.05);">
          <img src="/images/chapel-small.jpg" alt="Small Chapel at Britton Baptist Church" style="width:100%;height:180px;object-fit:cover;" loading="lazy">
          <div style="padding:20px;">
            <h4 style="font-family:'Nunito Sans',sans-serif;font-size:1rem;font-weight:700;color:var(--navy);margin-bottom:6px;">Chapel</h4>
            <p style="font-size:0.85rem;color:var(--text-soft);line-height:1.55;">Intimate chapel space for prayer, small group meetings, and quiet reflection.</p>
          </div>
        </div>

        <div style="background:white;border-radius:12px;overflow:hidden;border:1px solid rgba(0,0,0,0.05);">
          <img src="/images/nursery-room.jpg" alt="Children's Rooms at Britton Baptist Church" style="width:100%;height:180px;object-fit:cover;" loading="lazy">
          <div style="padding:20px;">
            <h4 style="font-family:'Nunito Sans',sans-serif;font-size:1rem;font-weight:700;color:var(--navy);margin-bottom:6px;">Library &amp; Classrooms</h4>
            <p style="font-size:0.85rem;color:var(--text-soft);line-height:1.55;">Church library and multiple classrooms for Sunday School, Bible study, and small group gatherings.</p>
          </div>
        </div>

      </div>
    </div>
  </section>

  <!-- Court Teaser -->
  <section class="sect" style="background:var(--cream);">"""

c = c.replace(old_court_teaser, new_facilities)

with open('ministries.html', 'w') as f:
    f.write(c)
print("ministries.html updated with photos")


# ══════════════════════════════════════════════════════════════════════════
# COURT-RENTAL.HTML — Add gym photos
# ══════════════════════════════════════════════════════════════════════════

with open('court-rental.html', 'r') as f:
    c = f.read()

# Add gym photo to the court visual block — replace the SVG-only block
old_court_visual = """        <div style="background:var(--navy);border-radius:16px;padding:48px 40px;position:relative;overflow:hidden;min-height:420px;display:flex;flex-direction:column;justify-content:flex-end;">
          <svg style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);opacity:0.12;" width="200" height="260" viewBox="0 0 200 260" fill="none">
            <rect x="10" y="10" width="180" height="240" stroke="#C9A84C" stroke-width="2" rx="2"/>
            <line x1="10" y1="130" x2="190" y2="130" stroke="#C9A84C" stroke-width="2"/>
            <circle cx="100" cy="130" r="30" stroke="#C9A84C" stroke-width="2"/>
            <rect x="60" y="10" width="80" height="60" stroke="#C9A84C" stroke-width="2"/>
            <rect x="60" y="190" width="80" height="60" stroke="#C9A84C" stroke-width="2"/>
          </svg>
          <h3 style="font-family:'Cormorant Garamond',serif;color:white;font-size:1.7rem;margin-bottom:10px;position:relative;">Full-Size Hardwood Court</h3>
          <p style="color:rgba(255,255,255,0.5);font-size:0.92rem;line-height:1.6;position:relative;">Regulation hoops, hardwood floor, climate-controlled gym with restrooms, showers, and water fountains. Easy access from Britton Rd and I-235 with free parking.</p>
        </div>"""

new_court_visual = """        <div style="border-radius:16px;overflow:hidden;position:relative;min-height:420px;display:flex;flex-direction:column;justify-content:flex-end;">
          <img src="/images/gym-panoramic.jpg" alt="Indoor Basketball Court at Britton Baptist Church Oklahoma City" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;">
          <div style="position:relative;z-index:2;padding:40px;background:linear-gradient(transparent,rgba(0,0,0,0.8));">
            <h3 style="font-family:'Cormorant Garamond',serif;color:white;font-size:1.7rem;margin-bottom:10px;">Full-Size Indoor Court</h3>
            <p style="color:rgba(255,255,255,0.7);font-size:0.92rem;line-height:1.6;">Regulation hoops, court lines, bleachers, climate-controlled gym with restrooms, showers, and water fountains. Easy access from Britton Rd and I-235 with free parking.</p>
          </div>
        </div>"""

c = c.replace(old_court_visual, new_court_visual)

with open('court-rental.html', 'w') as f:
    f.write(c)
print("court-rental.html updated with photos")


# ══════════════════════════════════════════════════════════════════════════
# CONTACT.HTML — Add exterior photo as hero background
# ══════════════════════════════════════════════════════════════════════════

with open('contact.html', 'r') as f:
    c = f.read()

c = c.replace(
    '<section style="padding:120px 24px 60px;background:var(--deep-blue);text-align:center;">',
    '<section style="padding:120px 24px 60px;background-image:linear-gradient(rgba(15,31,61,0.85),rgba(15,31,61,0.9)),url(/images/exterior-sign.jpg);background-size:cover;background-position:center;text-align:center;">',
    1
)

with open('contact.html', 'w') as f:
    f.write(c)
print("contact.html updated with photos")

print("\nAll pages updated with real photos!")
