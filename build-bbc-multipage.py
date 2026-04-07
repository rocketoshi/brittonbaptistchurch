#!/usr/bin/env python3
"""
Generate BBC multi-page site from existing CSS and content.
Run from ~/brittonbaptistchurch/
"""

# Read existing CSS
with open('/tmp/bbc-css.txt', 'r') as f:
    css = f.read()

# Read existing content sections
with open('/tmp/bbc-home-content.txt', 'r') as f:
    home_raw = f.read()

with open('/tmp/bbc-court-content.txt', 'r') as f:
    court_raw = f.read()

# ── Shared components ─────────────────────────────────────────────────────

fonts = """  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&family=Nunito+Sans:ital,opsz,wght@0,6..12,300..700;1,6..12,300..700&display=swap" rel="stylesheet">
"""

def nav(active="home"):
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
        <div class="nav-brand-text">
          Britton Baptist
          <small>Walk in the Light</small>
        </div>
      </a>
      <ul class="nav-menu" id="navMenu">
{links}      </ul>
      <button class="burger" onclick="document.getElementById('navMenu').classList.toggle('open')" aria-label="Menu">
        <div></div><div></div><div></div>
      </button>
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

mobile_menu_js = """  <script>
    document.querySelectorAll('.nav-menu a').forEach(link => {
      link.addEventListener('click', () => { document.getElementById('navMenu').classList.remove('open'); });
    });
  </script>
"""

def make_page(title, description, keywords, canonical, og_title, schema, active_nav, body_content, extra_js=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="keywords" content="{keywords}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{canonical}">

  <meta property="og:title" content="{og_title}">
  <meta property="og:description" content="{description}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{canonical}">

{schema}
{fonts}
{css}
</head>
<body>

{nav(active_nav)}
{body_content}
{footer}
{mobile_menu_js}
{extra_js}
</body>
</html>
"""


# ══════════════════════════════════════════════════════════════════════════════
# 1. HOMEPAGE — Hero + preview cards linking to each section
# ══════════════════════════════════════════════════════════════════════════════

home_schema = """  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Church",
    "name": "Britton Baptist Church",
    "alternateName": "BBC",
    "description": "Southern Baptist church serving Oklahoma City since 1941. Worship, youth programs, community outreach, and indoor basketball court rental.",
    "url": "https://brittonbaptist.church",
    "telephone": "+1-405-842-3511",
    "address": { "@type": "PostalAddress", "streetAddress": "1141 W Britton Rd", "addressLocality": "Oklahoma City", "addressRegion": "OK", "postalCode": "73114", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 35.5659, "longitude": -97.5326 },
    "denomination": "Southern Baptist Convention",
    "hasMap": "https://www.google.com/maps?q=Britton+Baptist+Church+Oklahoma+City",
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": "Sunday", "opens": "09:30", "closes": "19:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": "Wednesday", "opens": "17:00", "closes": "19:30" }
    ]
  }
  </script>

  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      { "@type": "Question", "name": "What are the service times at Britton Baptist Church?", "acceptedAnswer": { "@type": "Answer", "text": "Sunday School 9:30 AM, Morning Worship 10:50 AM, Evening Worship 6:00 PM. Wednesday: Fellowship Meal 5:00 PM, Children & Youth 6:00 PM, Midweek Service 6:15 PM." } },
      { "@type": "Question", "name": "Where is Britton Baptist Church?", "acceptedAnswer": { "@type": "Answer", "text": "1141 W Britton Rd, Oklahoma City, OK 73114. North OKC near I-235 and Britton Rd. Free parking." } },
      { "@type": "Question", "name": "What denomination is Britton Baptist Church?", "acceptedAnswer": { "@type": "Answer", "text": "Southern Baptist Convention (SBC). A welcoming, multi-generational congregation." } },
      { "@type": "Question", "name": "Does Britton Baptist Church have a basketball court?", "acceptedAnswer": { "@type": "Answer", "text": "Yes. Indoor basketball court available for rent at $20/hr. Book online at brittonbaptist.church/court-rental.html." } }
    ]
  }
  </script>"""

home_body = """
  <!-- Hero -->
  <section class="hero">
    <div class="hero-beams"></div>
    <div class="hero-texture"></div>
    <div class="hero-inner">
      <div>
        <div class="hero-tag">Southern Baptist Church &bull; Est. 1941</div>
        <h1>Walk in the <em>Light</em></h1>
        <p class="hero-desc">Britton Baptist Church is a lighthouse of hope in North Oklahoma City. We are a multi-generational, welcoming congregation rooted in faith, fellowship, and serving our community.</p>
        <div class="hero-btns">
          <a href="/about.html" class="btn btn-gold">Plan Your Visit &rarr;</a>
          <a href="/court-rental.html" class="btn btn-ghost">Rent Our Court</a>
        </div>
      </div>
      <div class="hero-card">
        <div class="hero-card-head">
          <div class="dot"></div>
          <span>This Week at BBC</span>
        </div>
        <div class="hero-card-body">
          <h3>Service Times</h3>
          <div class="sched-divider">Sunday</div>
          <div class="sched-row"><span class="t">9:30 AM</span><span class="e">Sunday School</span></div>
          <div class="sched-row"><span class="t">10:50 AM</span><span class="e">Morning Worship</span></div>
          <div class="sched-row"><span class="t">6:00 PM</span><span class="e">Evening Worship</span></div>
          <div class="sched-divider">Wednesday</div>
          <div class="sched-row"><span class="t">5:00 PM</span><span class="e">Fellowship Meal</span></div>
          <div class="sched-row"><span class="t">6:00 PM</span><span class="e">Children & Youth</span></div>
          <div class="sched-row"><span class="t">6:15 PM</span><span class="e">Midweek Service</span></div>
        </div>
        <div class="hero-card-foot">
          <a href="tel:4058423511">Call (405) 842-3511 &rarr;</a>
        </div>
      </div>
    </div>
  </section>

  <!-- Preview Cards -->
  <section class="sect" style="background:var(--cream);">
    <div class="sect-inner" style="text-align:center;">
      <div class="label">Welcome to BBC</div>
      <h2 class="sect-title">A Lighthouse of Hope Since 1941</h2>
      <p class="sect-sub" style="margin:0 auto 48px;">For over 80 years, Britton Baptist Church has served North Oklahoma City with faith, fellowship, and love. Whether you're seeking worship, community, or a place to play — you're welcome here.</p>

      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:24px;text-align:left;">

        <a href="/about.html" style="text-decoration:none;color:inherit;">
          <div class="min-card" style="background:white;border:1px solid rgba(0,0,0,0.05);border-radius:14px;padding:32px 28px;transition:all 0.25s;cursor:pointer;" onmouseover="this.style.borderColor='var(--gold)';this.style.transform='translateY(-3px)'" onmouseout="this.style.borderColor='rgba(0,0,0,0.05)';this.style.transform='none'">
            <div style="width:48px;height:48px;border-radius:12px;background:rgba(44,74,124,0.08);display:flex;align-items:center;justify-content:center;font-size:22px;margin-bottom:18px;">&#9971;</div>
            <h4 style="font-family:'Nunito Sans',sans-serif;font-size:1.05rem;font-weight:700;color:var(--navy);margin-bottom:8px;">Our Story</h4>
            <p style="font-size:0.88rem;color:var(--text-soft);line-height:1.65;">Learn about our 80+ year history, our mission as a lighthouse of hope, and how to become a Christian.</p>
            <span style="display:inline-block;margin-top:12px;color:var(--gold);font-size:0.85rem;font-weight:600;">Learn More &rarr;</span>
          </div>
        </a>

        <a href="/ministries.html" style="text-decoration:none;color:inherit;">
          <div style="background:white;border:1px solid rgba(0,0,0,0.05);border-radius:14px;padding:32px 28px;transition:all 0.25s;cursor:pointer;" onmouseover="this.style.borderColor='var(--gold)';this.style.transform='translateY(-3px)'" onmouseout="this.style.borderColor='rgba(0,0,0,0.05)';this.style.transform='none'">
            <div style="width:48px;height:48px;border-radius:12px;background:rgba(122,56,40,0.08);display:flex;align-items:center;justify-content:center;font-size:22px;margin-bottom:18px;">&#129309;</div>
            <h4 style="font-family:'Nunito Sans',sans-serif;font-size:1.05rem;font-weight:700;color:var(--navy);margin-bottom:8px;">Ministries</h4>
            <p style="font-size:0.88rem;color:var(--text-soft);line-height:1.65;">Worship, youth programs, children's ministry, missions, outreach, and our community basketball court.</p>
            <span style="display:inline-block;margin-top:12px;color:var(--gold);font-size:0.85rem;font-weight:600;">Explore &rarr;</span>
          </div>
        </a>

        <a href="/court-rental.html" style="text-decoration:none;color:inherit;">
          <div style="background:white;border:1px solid rgba(0,0,0,0.05);border-radius:14px;padding:32px 28px;transition:all 0.25s;cursor:pointer;" onmouseover="this.style.borderColor='var(--gold)';this.style.transform='translateY(-3px)'" onmouseout="this.style.borderColor='rgba(0,0,0,0.05)';this.style.transform='none'">
            <div style="width:48px;height:48px;border-radius:12px;background:rgba(201,168,76,0.1);display:flex;align-items:center;justify-content:center;font-size:22px;margin-bottom:18px;">&#127936;</div>
            <h4 style="font-family:'Nunito Sans',sans-serif;font-size:1.05rem;font-weight:700;color:var(--navy);margin-bottom:8px;">Court Rental</h4>
            <p style="font-size:0.88rem;color:var(--text-soft);line-height:1.65;">Rent our indoor basketball court for $20/hr. Online booking, live streaming, and open to everyone.</p>
            <span style="display:inline-block;margin-top:12px;color:var(--gold);font-size:0.85rem;font-weight:600;">Book Now &rarr;</span>
          </div>
        </a>

      </div>
    </div>
  </section>

  <!-- Court Teaser -->
  <section class="sect" style="background:var(--warm-white);">
    <div class="sect-inner">
      <div class="court-teaser">
        <div>
          <h3>Our Gym is Open &mdash; <em>Rent the Court</em></h3>
          <p>Indoor basketball court available for pickup games, team practices, youth leagues, birthday parties, and community events. $20/hr with online booking and live streaming.</p>
          <a href="/court-rental.html" class="btn btn-gold">Court Rental Info &rarr;</a>
        </div>
        <div class="court-mini-features">
          <div class="cmf"><div class="cmf-icon">&#127936;</div><h5>Full-Size Court</h5><p>Hardwood floor</p></div>
          <div class="cmf"><div class="cmf-icon">&#128249;</div><h5>Live Streaming</h5><p>Pickup.Earth cameras</p></div>
          <div class="cmf"><div class="cmf-icon">&#128197;</div><h5>Book Online</h5><p>Sked.Earth</p></div>
          <div class="cmf"><div class="cmf-icon">&#127359;&#65039;</div><h5>Free Parking</h5><p>On-site lot</p></div>
        </div>
      </div>
    </div>
  </section>

  <!-- Quick Contact -->
  <section class="sect" style="background:var(--cream);">
    <div class="sect-inner" style="text-align:center;">
      <div class="label">Visit Us</div>
      <h2 class="sect-title">Come Walk in the Light</h2>
      <p class="sect-sub" style="margin:0 auto 32px;">1141 W Britton Rd, Oklahoma City, OK 73114 &bull; (405) 842-3511</p>
      <div style="display:flex;gap:16px;justify-content:center;flex-wrap:wrap;">
        <a href="/contact.html" class="btn btn-gold">Get Directions &rarr;</a>
        <a href="tel:4058423511" class="btn btn-ghost" style="border-color:var(--navy);color:var(--navy);">Call Us</a>
      </div>
    </div>
  </section>
"""

index = make_page(
    "Britton Baptist Church | Baptist Church in Oklahoma City, OK | Sunday Worship & Youth Ministry",
    "Britton Baptist Church — a welcoming Southern Baptist church in North Oklahoma City since 1941. Sunday School 9:30 AM, Morning Worship 10:50 AM. Youth ministry, community outreach, indoor basketball court rental. 1141 W Britton Rd, OKC 73114.",
    "Britton Baptist Church, Baptist church Oklahoma City, church near me OKC, SBC church Oklahoma City, Southern Baptist church OKC, Sunday worship Oklahoma City, youth ministry Oklahoma City, church 73114, church with basketball court OKC, family church Oklahoma City",
    "https://brittonbaptist.church/",
    "Britton Baptist Church | Baptist Church in Oklahoma City",
    home_schema, "home", home_body
)

# ══════════════════════════════════════════════════════════════════════════════
# 2. ABOUT PAGE
# ══════════════════════════════════════════════════════════════════════════════

about_body = """
  <section style="padding:120px 24px 60px;background:var(--deep-blue);text-align:center;">
    <div style="max-width:700px;margin:0 auto;">
      <div class="label" style="color:var(--gold);">Our Story</div>
      <h1 style="font-family:'Cormorant Garamond',serif;font-size:clamp(2.2rem,5vw,3.2rem);color:white;line-height:1.1;margin-bottom:16px;">A Lighthouse of Hope Since 1941</h1>
      <p style="color:rgba(255,255,255,0.5);font-size:1.05rem;line-height:1.7;">For over 80 years, Britton Baptist Church has been shining God's light in North Oklahoma City.</p>
    </div>
  </section>

  <section class="sect" style="background:var(--cream);">
    <div class="sect-inner">
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:start;">
        <div>
          <h2 class="sect-title">Our Mission</h2>
          <p style="font-size:0.95rem;color:var(--text-soft);line-height:1.8;margin-bottom:16px;">What began as a small congregation on Britton Road has grown into a vibrant, faith-driven community committed to serving people from all walks of life.</p>
          <p style="font-size:0.95rem;color:var(--text-soft);line-height:1.8;margin-bottom:16px;">We believe that God is still at work &mdash; in our church, in our neighborhood, and in the lives of everyone who walks through our doors. Whether you're searching for answers, looking for community, or deepening your faith, you're welcome here.</p>

          <div class="verse-block">
            <q>Walk in the light, as He is in the light, and we have fellowship with one another.</q>
            <cite>1 John 1:7</cite>
          </div>

          <p style="font-size:0.95rem;color:var(--text-soft);line-height:1.8;">Our doors are open to everyone. Come as you are and discover what it means to walk in the light together.</p>
        </div>

        <div class="abc-plan">
          <h3>How to Become a Christian</h3>
          <div class="abc-step">
            <div class="abc-letter">A</div>
            <div><h4>Admit to God you are a sinner</h4><p>Romans 3:23</p></div>
          </div>
          <div class="abc-step">
            <div class="abc-letter">B</div>
            <div><h4>Believe that Jesus died &amp; rose again</h4><p>Romans 5:8</p></div>
          </div>
          <div class="abc-step">
            <div class="abc-letter">C</div>
            <div><h4>Confess your faith in Jesus Christ</h4><p>Romans 10:9-13</p></div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="sect" style="background:var(--warm-white);text-align:center;">
    <div class="sect-inner">
      <h2 class="sect-title">Ready to Visit?</h2>
      <p class="sect-sub" style="margin:0 auto 32px;">We'd love to welcome you this Sunday. Sunday School starts at 9:30 AM.</p>
      <div style="display:flex;gap:16px;justify-content:center;flex-wrap:wrap;">
        <a href="/contact.html" class="btn btn-gold">Get Directions &rarr;</a>
        <a href="/ministries.html" class="btn btn-ghost" style="border-color:var(--navy);color:var(--navy);">Our Ministries</a>
      </div>
    </div>
  </section>
"""

about = make_page(
    "About Britton Baptist Church | Our Story | Oklahoma City SBC Church",
    "Learn about Britton Baptist Church — a Southern Baptist church serving Oklahoma City since 1941. Our mission, our faith, how to become a Christian, and why we're called a lighthouse of hope. 1141 W Britton Rd, OKC 73114.",
    "about Britton Baptist Church, our story, church history Oklahoma City, how to become a Christian, SBC church OKC, Baptist church mission, lighthouse of hope, faith community Oklahoma City",
    "https://brittonbaptist.church/about.html",
    "About Britton Baptist Church | Oklahoma City",
    "", "about", about_body
)

# ══════════════════════════════════════════════════════════════════════════════
# 3. MINISTRIES PAGE
# ══════════════════════════════════════════════════════════════════════════════

ministries_body = """
  <section style="padding:120px 24px 60px;background:var(--deep-blue);text-align:center;">
    <div style="max-width:700px;margin:0 auto;">
      <div class="label" style="color:var(--gold);">Ministries & Community</div>
      <h1 style="font-family:'Cormorant Garamond',serif;font-size:clamp(2.2rem,5vw,3.2rem);color:white;line-height:1.1;margin-bottom:16px;">Serving Oklahoma City Together</h1>
      <p style="color:rgba(255,255,255,0.5);font-size:1.05rem;line-height:1.7;">From children's ministry to community outreach, we meet people where they are.</p>
    </div>
  </section>

  <section class="sect" style="background:var(--cream);">
    <div class="sect-inner">
      <div class="min-cards" style="display:grid;grid-template-columns:repeat(3,1fr);gap:24px;">
        <article class="min-card" style="background:white;border:1px solid rgba(0,0,0,0.05);border-radius:14px;padding:32px 28px;">
          <div style="width:48px;height:48px;border-radius:12px;background:rgba(44,74,124,0.08);display:flex;align-items:center;justify-content:center;font-size:22px;margin-bottom:18px;">&#9971;</div>
          <h4 style="font-family:'Nunito Sans',sans-serif;font-size:1.05rem;font-weight:700;color:var(--navy);margin-bottom:8px;">Worship &amp; Teaching</h4>
          <p style="font-size:0.88rem;color:var(--text-soft);line-height:1.65;">Passionate worship spanning multiple genres and expository Bible teaching. Sunday mornings and evenings, plus Wednesday midweek service with Pastor Belicek.</p>
        </article>
        <article style="background:white;border:1px solid rgba(0,0,0,0.05);border-radius:14px;padding:32px 28px;">
          <div style="width:48px;height:48px;border-radius:12px;background:rgba(122,56,40,0.08);display:flex;align-items:center;justify-content:center;font-size:22px;margin-bottom:18px;">&#128102;</div>
          <h4 style="font-family:'Nunito Sans',sans-serif;font-size:1.05rem;font-weight:700;color:var(--navy);margin-bottom:8px;">Children &amp; Youth</h4>
          <p style="font-size:0.88rem;color:var(--text-soft);line-height:1.65;">Age-appropriate programs for kids and teens every Wednesday evening and Sunday morning. Building faith, friendships, and character in a safe environment.</p>
        </article>
        <article style="background:white;border:1px solid rgba(0,0,0,0.05);border-radius:14px;padding:32px 28px;">
          <div style="width:48px;height:48px;border-radius:12px;background:rgba(201,168,76,0.1);display:flex;align-items:center;justify-content:center;font-size:22px;margin-bottom:18px;">&#129309;</div>
          <h4 style="font-family:'Nunito Sans',sans-serif;font-size:1.05rem;font-weight:700;color:var(--navy);margin-bottom:8px;">Missions &amp; Outreach</h4>
          <p style="font-size:0.88rem;color:var(--text-soft);line-height:1.65;">Serving our neighbors locally and globally &mdash; from food drives and community events in OKC to international missions reaching as far as the Philippines.</p>
        </article>
      </div>
    </div>
  </section>

  <!-- Service Times -->
  <section class="sect" style="background:var(--warm-white);">
    <div class="sect-inner" style="max-width:600px;">
      <div style="background:white;border-radius:16px;overflow:hidden;border:1px solid rgba(0,0,0,0.06);">
        <div style="background:var(--navy);padding:24px 28px;">
          <h3 style="font-family:'Cormorant Garamond',serif;color:white;font-size:1.3rem;">Service Times &amp; Schedule</h3>
        </div>
        <div style="padding:28px;">
          <div style="margin-bottom:28px;">
            <h4 style="font-size:0.82rem;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:var(--gold);margin-bottom:12px;padding-bottom:8px;border-bottom:1px solid rgba(0,0,0,0.06);">Sunday</h4>
            <div style="display:flex;justify-content:space-between;padding:8px 0;font-size:0.92rem;"><span style="font-weight:600;color:var(--navy);">9:30 AM</span><span style="color:var(--text-soft);">Sunday School</span></div>
            <div style="display:flex;justify-content:space-between;padding:8px 0;font-size:0.92rem;"><span style="font-weight:600;color:var(--navy);">10:50 AM</span><span style="color:var(--text-soft);">Morning Worship</span></div>
            <div style="display:flex;justify-content:space-between;padding:8px 0;font-size:0.92rem;"><span style="font-weight:600;color:var(--navy);">6:00 PM</span><span style="color:var(--text-soft);">Evening Worship</span></div>
          </div>
          <div>
            <h4 style="font-size:0.82rem;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:var(--gold);margin-bottom:12px;padding-bottom:8px;border-bottom:1px solid rgba(0,0,0,0.06);">Wednesday</h4>
            <div style="display:flex;justify-content:space-between;padding:8px 0;font-size:0.92rem;"><span style="font-weight:600;color:var(--navy);">5:00 PM</span><span style="color:var(--text-soft);">Fellowship Meal</span></div>
            <div style="display:flex;justify-content:space-between;padding:8px 0;font-size:0.92rem;"><span style="font-weight:600;color:var(--navy);">6:00 PM</span><span style="color:var(--text-soft);">Children &amp; Youth</span></div>
            <div style="display:flex;justify-content:space-between;padding:8px 0;font-size:0.92rem;"><span style="font-weight:600;color:var(--navy);">6:15 PM</span><span style="color:var(--text-soft);">Midweek Service</span></div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Court Teaser -->
  <section class="sect" style="background:var(--cream);">
    <div class="sect-inner">
      <div class="court-teaser">
        <div>
          <h3>Our Gym is Open &mdash; <em>Rent the Court</em></h3>
          <p>Indoor basketball court available for pickup games, team practices, youth leagues, and events. $20/hr with online booking.</p>
          <a href="/court-rental.html" class="btn btn-gold">Book a Court &rarr;</a>
        </div>
        <div class="court-mini-features">
          <div class="cmf"><div class="cmf-icon">&#127936;</div><h5>Full-Size Court</h5><p>Hardwood floor</p></div>
          <div class="cmf"><div class="cmf-icon">&#128249;</div><h5>Live Streaming</h5><p>Pickup.Earth</p></div>
          <div class="cmf"><div class="cmf-icon">&#128197;</div><h5>Book Online</h5><p>Sked.Earth</p></div>
          <div class="cmf"><div class="cmf-icon">&#127359;&#65039;</div><h5>Free Parking</h5><p>On-site lot</p></div>
        </div>
      </div>
    </div>
  </section>
"""

ministries = make_page(
    "Ministries at Britton Baptist Church | Youth Programs, Worship & Outreach | OKC",
    "Explore ministries at Britton Baptist Church in Oklahoma City. Sunday worship, youth and children's programs, Wednesday services, missions and community outreach. Everyone welcome.",
    "church ministries Oklahoma City, youth ministry OKC, children's ministry Oklahoma City, Sunday worship OKC, Wednesday church service, church outreach Oklahoma City, Pastor Belicek, Bible study OKC",
    "https://brittonbaptist.church/ministries.html",
    "Ministries at Britton Baptist Church | Oklahoma City",
    "", "ministries", ministries_body
)

# ══════════════════════════════════════════════════════════════════════════════
# 4. CONTACT PAGE
# ══════════════════════════════════════════════════════════════════════════════

contact_body = """
  <section style="padding:120px 24px 60px;background:var(--deep-blue);text-align:center;">
    <div style="max-width:700px;margin:0 auto;">
      <div class="label" style="color:var(--gold);">Visit Us</div>
      <h1 style="font-family:'Cormorant Garamond',serif;font-size:clamp(2.2rem,5vw,3.2rem);color:white;line-height:1.1;margin-bottom:16px;">Come Walk in the Light</h1>
      <p style="color:rgba(255,255,255,0.5);font-size:1.05rem;line-height:1.7;">We'd love to welcome you &mdash; to a service, a community event, or a pickup game.</p>
    </div>
  </section>

  <section class="sect" style="background:var(--cream);">
    <div class="sect-inner">
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:48px;">
        <div style="display:flex;flex-direction:column;gap:24px;">
          <div style="display:flex;gap:14px;align-items:flex-start;">
            <div style="width:44px;height:44px;border-radius:10px;background:rgba(201,168,76,0.08);display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0;">&#128205;</div>
            <div><h4 style="font-family:'Nunito Sans',sans-serif;font-size:0.95rem;font-weight:700;color:var(--navy);margin-bottom:2px;">Address</h4><p style="font-size:0.9rem;color:var(--text-soft);line-height:1.5;">1141 W Britton Rd<br>Oklahoma City, OK 73114</p></div>
          </div>
          <div style="display:flex;gap:14px;align-items:flex-start;">
            <div style="width:44px;height:44px;border-radius:10px;background:rgba(201,168,76,0.08);display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0;">&#128222;</div>
            <div><h4 style="font-family:'Nunito Sans',sans-serif;font-size:0.95rem;font-weight:700;color:var(--navy);margin-bottom:2px;">Phone</h4><a href="tel:4058423511" style="font-size:0.9rem;color:var(--text-soft);text-decoration:none;">(405) 842-3511</a></div>
          </div>
          <div style="display:flex;gap:14px;align-items:flex-start;">
            <div style="width:44px;height:44px;border-radius:10px;background:rgba(201,168,76,0.08);display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0;">&#128336;</div>
            <div><h4 style="font-family:'Nunito Sans',sans-serif;font-size:0.95rem;font-weight:700;color:var(--navy);margin-bottom:2px;">Sunday Services</h4><p style="font-size:0.9rem;color:var(--text-soft);line-height:1.5;">9:30 AM, 10:50 AM, 6:00 PM</p></div>
          </div>
          <div style="display:flex;gap:14px;align-items:flex-start;">
            <div style="width:44px;height:44px;border-radius:10px;background:rgba(201,168,76,0.08);display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0;">&#127860;</div>
            <div><h4 style="font-family:'Nunito Sans',sans-serif;font-size:0.95rem;font-weight:700;color:var(--navy);margin-bottom:2px;">Wednesday</h4><p style="font-size:0.9rem;color:var(--text-soft);line-height:1.5;">Meal 5PM &bull; Youth 6PM &bull; Service 6:15PM</p></div>
          </div>
          <div style="display:flex;gap:14px;align-items:flex-start;">
            <div style="width:44px;height:44px;border-radius:10px;background:rgba(201,168,76,0.08);display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0;">&#9971;</div>
            <div><h4 style="font-family:'Nunito Sans',sans-serif;font-size:0.95rem;font-weight:700;color:var(--navy);margin-bottom:2px;">Denomination</h4><p style="font-size:0.9rem;color:var(--text-soft);line-height:1.5;">Southern Baptist Convention (SBC)</p></div>
          </div>
          <div style="display:flex;gap:14px;align-items:flex-start;">
            <div style="width:44px;height:44px;border-radius:10px;background:rgba(201,168,76,0.08);display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0;">&#127936;</div>
            <div><h4 style="font-family:'Nunito Sans',sans-serif;font-size:0.95rem;font-weight:700;color:var(--navy);margin-bottom:2px;">Court Rental</h4><a href="/court-rental.html" style="font-size:0.9rem;color:var(--gold);text-decoration:none;">Book at $20/hr &rarr;</a></div>
          </div>
        </div>
        <div style="border-radius:12px;overflow:hidden;border:1px solid rgba(0,0,0,0.06);min-height:400px;">
          <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3238.5!2d-97.535!3d35.566!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x87b21bdc87d8c78d%3A0xb0d77a6a8bfbda03!2sBritton%20Baptist%20Church!5e0!3m2!1sen!2sus!4v1" width="100%" height="100%" style="border:none;min-height:400px;" loading="lazy" title="Britton Baptist Church Location - 1141 W Britton Rd Oklahoma City"></iframe>
        </div>
      </div>
    </div>
  </section>
"""

contact = make_page(
    "Contact & Directions | Britton Baptist Church | 1141 W Britton Rd OKC 73114",
    "Visit Britton Baptist Church at 1141 W Britton Rd, Oklahoma City, OK 73114. Sunday School 9:30 AM, Worship 10:50 AM. Call (405) 842-3511. Free parking, near I-235 and Britton Rd.",
    "Britton Baptist Church address, directions to Britton Baptist Church, church Oklahoma City 73114, church near me north OKC, church Britton Road, church near I-235 OKC",
    "https://brittonbaptist.church/contact.html",
    "Contact Britton Baptist Church | Oklahoma City",
    "", "contact", contact_body
)

# ══════════════════════════════════════════════════════════════════════════════
# WRITE ALL FILES
# ══════════════════════════════════════════════════════════════════════════════

for name, content in [("index.html", index), ("about.html", about), ("ministries.html", ministries), ("contact.html", contact)]:
    with open(name, 'w') as f:
        f.write(content)
    print(f"{name} written ({len(content):,} chars)")

# Update sitemap
sitemap = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://brittonbaptist.church/</loc><lastmod>2026-04-07</lastmod><changefreq>weekly</changefreq><priority>1.0</priority></url>
  <url><loc>https://brittonbaptist.church/about.html</loc><lastmod>2026-04-07</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>
  <url><loc>https://brittonbaptist.church/ministries.html</loc><lastmod>2026-04-07</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>
  <url><loc>https://brittonbaptist.church/court-rental.html</loc><lastmod>2026-04-07</lastmod><changefreq>daily</changefreq><priority>0.9</priority></url>
  <url><loc>https://brittonbaptist.church/contact.html</loc><lastmod>2026-04-07</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>
</urlset>
"""
with open('sitemap.xml', 'w') as f:
    f.write(sitemap)
print("sitemap.xml updated")

print("\nDone! All pages generated.")
