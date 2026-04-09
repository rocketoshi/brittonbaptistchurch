#!/usr/bin/env python3
"""
Generate facility pages + update all BBC pages with all 48 photos.
Run from ~/brittonbaptistchurch/
Requires: existing pages from build-bbc-multipage.py already in place
"""

# Read CSS from index.html
with open('index.html', 'r') as f:
    full_index = f.read()

# Extract everything from <style> to </style>
style_start = full_index.find('<style>')
style_end = full_index.find('</style>') + 8
css_block = full_index[style_start:style_end]

fonts = """  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&family=Nunito+Sans:ital,opsz,wght@0,6..12,300..700;1,6..12,300..700&display=swap" rel="stylesheet">
"""

def nav_html(active=""):
    items = [
        ("home", "/", "Home"),
        ("about", "/about.html", "About"),
        ("ministries", "/ministries.html", "Ministries"),
        ("court", "/court-rental.html", "Court Rental"),
        ("contact", "/contact.html", "Contact"),
    ]
    links = ""
    for key, href, label in items:
        style = ' style="color:var(--gold);"' if key == active else ''
        links += f'        <li><a href="{href}"{style}>{label}</a></li>\n'
    links += '        <li><a href="/court-rental.html#booking" class="nav-cta">Book a Court</a></li>\n'
    return f"""  <nav class="site-nav">
    <div class="nav-wrap">
      <a href="/" class="nav-brand">
        <div class="lighthouse-icon">
          <svg viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="13" y="8" width="10" height="22" rx="1" fill="#C9A84C" opacity="0.9"/>
            <rect x="15" y="4" width="6" height="6" rx="1" fill="#E2C86D"/>
            <rect x="17" y="1" width="2" height="4" rx="1" fill="#E2C86D"/>
            <rect x="10" y="30" width="16" height="4" rx="1" fill="#C9A84C" opacity="0.7"/>
            <rect x="16" y="14" width="4" height="4" rx="0.5" fill="#0F1F3D"/>
            <rect x="16" y="21" width="4" height="4" rx="0.5" fill="#0F1F3D"/>
            <line x1="12" y1="6" x2="4" y2="2" stroke="#E2C86D" stroke-width="1" opacity="0.5"/>
            <line x1="24" y1="6" x2="32" y2="2" stroke="#E2C86D" stroke-width="1" opacity="0.5"/>
            <line x1="12" y1="8" x2="2" y2="8" stroke="#E2C86D" stroke-width="1" opacity="0.3"/>
            <line x1="24" y1="8" x2="34" y2="8" stroke="#E2C86D" stroke-width="1" opacity="0.3"/>
          </svg>
        </div>
        <div class="nav-brand-text">Britton Baptist<small>Walk in the Light</small></div>
      </a>
      <ul class="nav-menu" id="navMenu">
{links}      </ul>
      <button class="burger" onclick="document.getElementById('navMenu').classList.toggle('open')" aria-label="Menu"><div></div><div></div><div></div></button>
    </div>
  </nav>
"""

footer = """  <footer class="site-footer">
    <div class="footer-inner">
      <p>&copy; 2026 Britton Baptist Church &middot; 1141 W Britton Rd, Oklahoma City, OK 73114 &middot; <a href="tel:4058423511">(405) 842-3511</a></p>
      <p>Court booking by <a href="https://sked.earth" target="_blank">Sked.Earth</a> &middot; Streaming by <a href="https://pickup.earth" target="_blank">Pickup.Earth</a></p>
    </div>
  </footer>
"""

base_js = """  <script>
    document.querySelectorAll('.nav-menu a').forEach(link => {
      link.addEventListener('click', () => { document.getElementById('navMenu').classList.remove('open'); });
    });
  </script>
"""

def photo_gallery(images, cols=3):
    """images = list of (filename, alt) tuples"""
    items = "\n".join([f'          <img src="/images/{f}" alt="{a}" style="border-radius:8px;width:100%;height:240px;object-fit:cover;" loading="lazy">' for f, a in images])
    return f"""      <div style="display:grid;grid-template-columns:repeat({cols},1fr);gap:10px;margin-top:24px;">
{items}
      </div>"""

def facility_page(title, meta_desc, keywords, canonical, hero_img, hero_title, hero_sub, breadcrumb_name, body_content):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{meta_desc}">
  <meta name="keywords" content="{keywords}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{canonical}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{meta_desc}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{canonical}">
{fonts}
{css_block}
</head>
<body>

{nav_html("ministries")}

  <section style="padding:120px 24px 60px;background-image:linear-gradient(rgba(15,31,61,0.82),rgba(15,31,61,0.88)),url(/images/{hero_img});background-size:cover;background-position:center;text-align:center;">
    <div style="max-width:700px;margin:0 auto;">
      <nav style="font-size:0.78rem;color:rgba(255,255,255,0.35);margin-bottom:20px;">
        <a href="/" style="color:var(--gold);text-decoration:none;">Home</a> / <a href="/ministries.html" style="color:var(--gold);text-decoration:none;">Ministries</a> / {breadcrumb_name}
      </nav>
      <h1 style="font-family:'Cormorant Garamond',serif;font-size:clamp(2rem,4.5vw,3rem);color:white;line-height:1.1;margin-bottom:16px;">{hero_title}</h1>
      <p style="color:rgba(255,255,255,0.5);font-size:1.05rem;line-height:1.7;">{hero_sub}</p>
    </div>
  </section>

{body_content}

  <!-- Other Facilities -->
  <section class="sect" style="background:var(--cream);">
    <div class="sect-inner" style="text-align:center;">
      <h2 class="sect-title">Explore Our Campus</h2>
      <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:24px;">
        <a href="/sanctuary.html" style="padding:10px 20px;background:var(--navy);color:white;border-radius:8px;text-decoration:none;font-size:0.85rem;font-weight:600;">Sanctuary</a>
        <a href="/chapel.html" style="padding:10px 20px;background:var(--navy);color:white;border-radius:8px;text-decoration:none;font-size:0.85rem;font-weight:600;">Chapel</a>
        <a href="/daycare.html" style="padding:10px 20px;background:var(--navy);color:white;border-radius:8px;text-decoration:none;font-size:0.85rem;font-weight:600;">Nursery &amp; Daycare</a>
        <a href="/sewing-club.html" style="padding:10px 20px;background:var(--navy);color:white;border-radius:8px;text-decoration:none;font-size:0.85rem;font-weight:600;">Sewing Club</a>
        <a href="/food-pantry.html" style="padding:10px 20px;background:var(--navy);color:white;border-radius:8px;text-decoration:none;font-size:0.85rem;font-weight:600;">Food Pantry</a>
        <a href="/fellowship-hall.html" style="padding:10px 20px;background:var(--navy);color:white;border-radius:8px;text-decoration:none;font-size:0.85rem;font-weight:600;">Fellowship Hall</a>
        <a href="/court-rental.html" style="padding:10px 20px;background:var(--gold);color:var(--navy);border-radius:8px;text-decoration:none;font-size:0.85rem;font-weight:600;">Basketball Court</a>
      </div>
    </div>
  </section>

{footer}
{base_js}
</body>
</html>
"""

# ══════════════════════════════════════════════════════════════════════════
# SANCTUARY PAGE
# ══════════════════════════════════════════════════════════════════════════

sanctuary_body = f"""
  <section class="sect" style="background:var(--cream);">
    <div class="sect-inner">
      <h2 class="sect-title">Our Sanctuary</h2>
      <p style="font-size:0.95rem;color:var(--text-soft);line-height:1.8;max-width:700px;margin-bottom:8px;">The heart of Britton Baptist Church. Our sanctuary seats hundreds for Sunday morning worship, evening services, and special events. Traditional architecture with modern sound and lighting for a powerful worship experience.</p>
      <p style="font-size:0.95rem;color:var(--text-soft);line-height:1.8;max-width:700px;">Services feature passionate worship spanning multiple genres and expository Bible teaching by Pastor Belicek. Everyone is welcome.</p>
{photo_gallery([
    ("sanctuary-01.jpg", "Britton Baptist Church sanctuary view from back"),
    ("sanctuary-02.jpg", "Sanctuary pews at Britton Baptist Church"),
    ("sanctuary-03.jpg", "Britton Baptist Church sanctuary interior"),
], 3)}
{photo_gallery([
    ("sanctuary-04.jpg", "Sanctuary seating at Britton Baptist Church Oklahoma City"),
    ("sanctuary-05.jpg", "Britton Baptist Church worship space"),
    ("sanctuary-06-stage.jpg", "Pulpit and stage at Britton Baptist Church"),
], 3)}
    </div>
  </section>

  <section class="sect" style="background:var(--warm-white);text-align:center;">
    <div class="sect-inner">
      <h2 class="sect-title">Join Us for Worship</h2>
      <p class="sect-sub" style="margin:0 auto 24px;">Sunday School 9:30 AM &bull; Morning Worship 10:50 AM &bull; Evening Worship 6:00 PM</p>
      <a href="/contact.html" class="btn btn-gold">Get Directions &rarr;</a>
    </div>
  </section>
"""

with open('sanctuary.html', 'w') as f:
    f.write(facility_page(
        "Sanctuary | Britton Baptist Church | Worship Space Oklahoma City",
        "Experience worship at Britton Baptist Church sanctuary in Oklahoma City. Traditional architecture, modern sound, passionate worship. Sunday School 9:30 AM, Morning Worship 10:50 AM. 1141 W Britton Rd.",
        "Britton Baptist Church sanctuary, church worship Oklahoma City, Sunday worship OKC, church sanctuary north OKC",
        "https://brittonbaptist.church/sanctuary.html",
        "sanctuary-01.jpg", "Our Sanctuary", "Where we gather to worship, learn, and grow together.",
        "Sanctuary", sanctuary_body
    ))
print("sanctuary.html created")

# ══════════════════════════════════════════════════════════════════════════
# CHAPEL PAGE
# ══════════════════════════════════════════════════════════════════════════

chapel_body = f"""
  <section class="sect" style="background:var(--cream);">
    <div class="sect-inner">
      <h2 class="sect-title">The Chapel</h2>
      <p style="font-size:0.95rem;color:var(--text-soft);line-height:1.8;max-width:700px;margin-bottom:8px;">An intimate space for prayer, small group meetings, and quiet reflection. The chapel provides a peaceful setting for personal devotion, smaller gatherings, and midweek prayer sessions.</p>
{photo_gallery([("chapel-01.jpg", "Small chapel at Britton Baptist Church Oklahoma City")], 1)}
    </div>
  </section>
"""

with open('chapel.html', 'w') as f:
    f.write(facility_page(
        "Chapel | Britton Baptist Church | Prayer Room Oklahoma City",
        "Intimate chapel at Britton Baptist Church for prayer, small groups, and reflection. A peaceful space in North Oklahoma City. 1141 W Britton Rd.",
        "church chapel Oklahoma City, prayer room OKC, small group meeting space church, Britton Baptist chapel",
        "https://brittonbaptist.church/chapel.html",
        "chapel-01.jpg", "The Chapel", "A quiet space for prayer, reflection, and small gatherings.",
        "Chapel", chapel_body
    ))
print("chapel.html created")

# ══════════════════════════════════════════════════════════════════════════
# DAYCARE PAGE
# ══════════════════════════════════════════════════════════════════════════

daycare_body = f"""
  <section class="sect" style="background:var(--cream);">
    <div class="sect-inner">
      <h2 class="sect-title">Nursery &amp; Daycare</h2>
      <p style="font-size:0.95rem;color:var(--text-soft);line-height:1.8;max-width:700px;margin-bottom:8px;">Britton Baptist Church provides safe, loving childcare with multiple dedicated rooms for infants, toddlers, and young children. Our nursery and daycare facilities are staffed by caring volunteers during all services and church events.</p>
      <p style="font-size:0.95rem;color:var(--text-soft);line-height:1.8;max-width:700px;">Parents can worship with peace of mind knowing their children are in a nurturing, age-appropriate environment with toys, activities, and individual attention.</p>
{photo_gallery([
    ("daycare-01.jpg", "Daycare room at Britton Baptist Church"),
    ("daycare-02.jpg", "Nursery at Britton Baptist Church Oklahoma City"),
    ("daycare-03.jpg", "Children's classroom at Britton Baptist Church"),
], 3)}
{photo_gallery([
    ("daycare-04.jpg", "Nursery room Britton Baptist Church OKC"),
    ("daycare-05.jpg", "Daycare space at Britton Baptist Church"),
    ("daycare-06.jpg", "Children's area Britton Baptist Church"),
], 3)}
{photo_gallery([
    ("daycare-07.jpg", "Kids room at Britton Baptist Church Oklahoma City"),
    ("daycare-08.jpg", "Nursery facility Britton Baptist Church"),
    ("daycare-09.jpg", "Childcare room Britton Baptist Church"),
], 3)}
{photo_gallery([
    ("daycare-10.jpg", "Daycare facility at Britton Baptist Church OKC"),
    ("daycare-11.jpg", "Children's ministry room Britton Baptist Church"),
], 2)}
    </div>
  </section>
"""

with open('daycare.html', 'w') as f:
    f.write(facility_page(
        "Nursery & Daycare | Britton Baptist Church | Childcare Oklahoma City",
        "Safe, loving nursery and daycare at Britton Baptist Church in Oklahoma City. Multiple rooms for infants and toddlers. Childcare during all services and events. 1141 W Britton Rd, OKC 73114.",
        "church daycare Oklahoma City, church nursery OKC, childcare during church service, church with daycare north OKC, Britton Baptist daycare, children's ministry Oklahoma City",
        "https://brittonbaptist.church/daycare.html",
        "daycare-01.jpg", "Nursery &amp; Daycare", "Safe, loving childcare for your little ones during every service and event.",
        "Nursery &amp; Daycare", daycare_body
    ))
print("daycare.html created")

# ══════════════════════════════════════════════════════════════════════════
# SEWING CLUB PAGE
# ══════════════════════════════════════════════════════════════════════════

sewing_body = f"""
  <section class="sect" style="background:var(--cream);">
    <div class="sect-inner">
      <h2 class="sect-title">Sewing &amp; Quilting Club</h2>
      <p style="font-size:0.95rem;color:var(--text-soft);line-height:1.8;max-width:700px;margin-bottom:8px;">One of Britton Baptist Church's most vibrant ministries. Our sewing and quilting club brings together women of all ages to create beautiful quilts, clothing, and crafts — many of which are donated to those in need across Oklahoma City.</p>
      <p style="font-size:0.95rem;color:var(--text-soft);line-height:1.8;max-width:700px;">With dedicated rooms, sewing machines, and a welcoming community of crafters, our sewing ministry is a place of creativity, fellowship, and service. Beginners and experienced quilters alike are welcome.</p>
{photo_gallery([
    ("sewing-01.jpg", "Sewing club at Britton Baptist Church"),
    ("sewing-02.jpg", "Sewing machines at Britton Baptist Church OKC"),
    ("sewing-03.jpg", "Quilting at Britton Baptist Church Oklahoma City"),
], 3)}
{photo_gallery([
    ("sewing-04.jpg", "Sewing ministry Britton Baptist Church"),
    ("sewing-05.jpg", "Quilting room at Britton Baptist Church"),
    ("sewing-06.jpg", "Sewing club room Britton Baptist Church OKC"),
], 3)}
{photo_gallery([
    ("sewing-07.jpg", "Quilts at Britton Baptist Church Oklahoma City"),
    ("sewing-08.jpg", "Sewing group at Britton Baptist Church"),
    ("sewing-09.jpg", "Fabric and supplies at Britton Baptist sewing ministry"),
], 3)}
{photo_gallery([
    ("sewing-10.jpg", "Sewing room at Britton Baptist Church OKC"),
    ("sewing-11.jpg", "Quilting projects Britton Baptist Church"),
    ("sewing-12.jpg", "Sewing and knitting club Britton Baptist Church"),
], 3)}
    </div>
  </section>
"""

with open('sewing-club.html', 'w') as f:
    f.write(facility_page(
        "Sewing & Quilting Club | Britton Baptist Church | Oklahoma City",
        "Join the sewing and quilting club at Britton Baptist Church in Oklahoma City. Dedicated sewing rooms, machines, and a welcoming community. Create quilts and crafts for the community. All skill levels welcome.",
        "church sewing club Oklahoma City, quilting group OKC, sewing ministry, church quilting club, Britton Baptist sewing, knitting group Oklahoma City, craft ministry OKC",
        "https://brittonbaptist.church/sewing-club.html",
        "sewing-01.jpg", "Sewing &amp; Quilting Club", "Creativity, fellowship, and service — one stitch at a time.",
        "Sewing &amp; Quilting Club", sewing_body
    ))
print("sewing-club.html created")

# ══════════════════════════════════════════════════════════════════════════
# FOOD PANTRY PAGE
# ══════════════════════════════════════════════════════════════════════════

food_body = f"""
  <section class="sect" style="background:var(--cream);">
    <div class="sect-inner">
      <h2 class="sect-title">Food Pantry</h2>
      <p style="font-size:0.95rem;color:var(--text-soft);line-height:1.8;max-width:700px;margin-bottom:8px;">Britton Baptist Church operates a food pantry serving families in need across North Oklahoma City. Stocked with non-perishable food items, the pantry is open to anyone in the community — no church membership required.</p>
      <p style="font-size:0.95rem;color:var(--text-soft);line-height:1.8;max-width:700px;">If you or someone you know needs food assistance, please contact us at (405) 842-3511. Donations of non-perishable food items are always welcome.</p>
{photo_gallery([("food-pantry-01.jpg", "Food pantry at Britton Baptist Church Oklahoma City")], 1)}
    </div>
  </section>

  <section class="sect" style="background:var(--warm-white);text-align:center;">
    <div class="sect-inner">
      <h2 class="sect-title">Need Help? Want to Help?</h2>
      <p class="sect-sub" style="margin:0 auto 24px;">Our food pantry is here for the community. Contact us to receive assistance or to donate.</p>
      <a href="tel:4058423511" class="btn btn-gold">Call (405) 842-3511</a>
    </div>
  </section>
"""

with open('food-pantry.html', 'w') as f:
    f.write(facility_page(
        "Food Pantry | Britton Baptist Church | Free Food Assistance Oklahoma City",
        "Free food pantry at Britton Baptist Church in Oklahoma City. Non-perishable food assistance for families in need. No membership required. Open to the community. 1141 W Britton Rd, OKC 73114. Call (405) 842-3511.",
        "church food pantry Oklahoma City, free food assistance OKC, food bank north Oklahoma City, food pantry near me 73114, Britton Baptist food pantry, community food assistance OKC",
        "https://brittonbaptist.church/food-pantry.html",
        "food-pantry-01.jpg", "Food Pantry", "Serving families in need across North Oklahoma City.",
        "Food Pantry", food_body
    ))
print("food-pantry.html created")

# ══════════════════════════════════════════════════════════════════════════
# FELLOWSHIP HALL PAGE
# ══════════════════════════════════════════════════════════════════════════

fellowship_body = f"""
  <section class="sect" style="background:var(--cream);">
    <div class="sect-inner">
      <h2 class="sect-title">Fellowship Hall &amp; Kitchen</h2>
      <p style="font-size:0.95rem;color:var(--text-soft);line-height:1.8;max-width:700px;margin-bottom:8px;">Our fellowship hall is the social heart of Britton Baptist Church. A large, open cafeteria space with a full commercial kitchen, it hosts our Wednesday fellowship meals, church dinners, community events, and celebrations.</p>
      <p style="font-size:0.95rem;color:var(--text-soft);line-height:1.8;max-width:700px;">The Wednesday Fellowship Meal at 5:00 PM is a beloved tradition — come enjoy a home-cooked meal with your church family before youth programs and midweek service.</p>
{photo_gallery([
    ("cafeteria-01.jpg", "Fellowship hall cafeteria at Britton Baptist Church"),
    ("kitchen-01.jpg", "Commercial kitchen at Britton Baptist Church Oklahoma City"),
], 2)}
    </div>
  </section>
"""

with open('fellowship-hall.html', 'w') as f:
    f.write(facility_page(
        "Fellowship Hall & Kitchen | Britton Baptist Church | Oklahoma City",
        "Fellowship hall and commercial kitchen at Britton Baptist Church in Oklahoma City. Wednesday fellowship meals, church dinners, and community events. 1141 W Britton Rd.",
        "church fellowship hall Oklahoma City, church kitchen OKC, Wednesday church dinner, church cafeteria north OKC, community dinner Oklahoma City",
        "https://brittonbaptist.church/fellowship-hall.html",
        "cafeteria-01.jpg", "Fellowship Hall &amp; Kitchen", "Where we break bread together as a church family.",
        "Fellowship Hall", fellowship_body
    ))
print("fellowship-hall.html created")

# ══════════════════════════════════════════════════════════════════════════
# UPDATE SITEMAP with all pages
# ══════════════════════════════════════════════════════════════════════════

sitemap = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://brittonbaptist.church/</loc><lastmod>2026-04-09</lastmod><changefreq>weekly</changefreq><priority>1.0</priority></url>
  <url><loc>https://brittonbaptist.church/about.html</loc><lastmod>2026-04-09</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>
  <url><loc>https://brittonbaptist.church/ministries.html</loc><lastmod>2026-04-09</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>
  <url><loc>https://brittonbaptist.church/court-rental.html</loc><lastmod>2026-04-09</lastmod><changefreq>daily</changefreq><priority>0.9</priority></url>
  <url><loc>https://brittonbaptist.church/contact.html</loc><lastmod>2026-04-09</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>
  <url><loc>https://brittonbaptist.church/sanctuary.html</loc><lastmod>2026-04-09</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>
  <url><loc>https://brittonbaptist.church/chapel.html</loc><lastmod>2026-04-09</lastmod><changefreq>monthly</changefreq><priority>0.6</priority></url>
  <url><loc>https://brittonbaptist.church/daycare.html</loc><lastmod>2026-04-09</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>
  <url><loc>https://brittonbaptist.church/sewing-club.html</loc><lastmod>2026-04-09</lastmod><changefreq>monthly</changefreq><priority>0.6</priority></url>
  <url><loc>https://brittonbaptist.church/food-pantry.html</loc><lastmod>2026-04-09</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>
  <url><loc>https://brittonbaptist.church/fellowship-hall.html</loc><lastmod>2026-04-09</lastmod><changefreq>monthly</changefreq><priority>0.6</priority></url>
</urlset>
"""
with open('sitemap.xml', 'w') as f:
    f.write(sitemap)
print("sitemap.xml updated with 11 pages")

print("\nAll facility pages created! Total pages: 11")
print("  - index.html (homepage)")
print("  - about.html")
print("  - ministries.html")
print("  - court-rental.html")
print("  - contact.html")
print("  - sanctuary.html")
print("  - chapel.html")
print("  - daycare.html")
print("  - sewing-club.html")
print("  - food-pantry.html")
print("  - fellowship-hall.html")
