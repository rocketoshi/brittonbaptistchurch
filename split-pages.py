#!/usr/bin/env python3
"""
Split BBC single-page site into two proper HTML files:
  - index.html (church homepage)
  - court-rental.html (SEO court rental page)
Run from ~/brittonbaptistchurch/
"""
import re

with open('index.html', 'r') as f:
    content = f.read()

# ── Extract shared parts ──────────────────────────────────────────────────
# Everything from start to the nav close
head_end = content.find('<!-- ========== NAVIGATION ==========')
nav_end = content.find('<!-- ================================\n       HOME PAGE')

# Get the head section (up to </head><body>)
head_match = content[:content.find('<body>') + 6]

# Get the nav section  
nav_start = content.find('<nav class="site-nav">')
nav_section_end = content.find('</nav>') + 6
nav_section = content[nav_start:nav_section_end]

# Get the footer
footer_start = content.find('<!-- ========== FOOTER ==========')
footer_section = content[footer_start:content.find('</body>')]

# Get the styles (everything between <style> and </style>)
style_start = content.find('<style>')
style_end = content.find('</style>') + 8
styles = content[style_start:style_end]

# Get page-home content
home_start = content.find('<div class="page active" id="page-home">')
home_end = content.find('</div><!-- /page-home -->') + len('</div><!-- /page-home -->')
home_content = content[home_start:home_end]

# Get page-court content
court_start = content.find('<div class="page" id="page-court">')
court_end = content.find('</div><!-- /page-court -->') + len('</div><!-- /page-court -->')
court_content = content[court_start:court_end]

# ── Build nav for multi-page (replace showPage calls with real links) ─────

nav_home = nav_section
nav_home = nav_home.replace("onclick=\"showPage('home');return false;\"", "href=\"/\"")
nav_home = nav_home.replace("onclick=\"showPage('home');scrollToId('about');return false;\"", "href=\"/#about\"")
nav_home = nav_home.replace("onclick=\"showPage('home');scrollToId('ministries');return false;\"", "href=\"/#ministries\"")
nav_home = nav_home.replace("onclick=\"showPage('court');return false;\"", "href=\"/court-rental.html\"")
nav_home = nav_home.replace("onclick=\"showPage('home');scrollToId('contact');return false;\"", "href=\"/#contact\"")
nav_home = nav_home.replace("onclick=\"showPage('court');scrollToId('booking');return false;\"", "href=\"/court-rental.html#booking\"")
# Fix the brand link
nav_home = nav_home.replace('<a href="#" class="nav-brand" href="/">', '<a href="/" class="nav-brand">')
nav_home = re.sub(r'<a href="#" class="nav-brand"[^>]*>', '<a href="/" class="nav-brand">', nav_home)

nav_court = nav_home  # Same nav for both pages

# ── Fix home content (remove page wrapper, fix internal links) ────────────
home_inner = home_content.replace('<div class="page active" id="page-home">', '')
home_inner = home_inner.replace('</div><!-- /page-home -->', '')
home_inner = home_inner.replace("onclick=\"showPage('home');scrollToId('about');return false;\"", "href=\"#about\"")
home_inner = home_inner.replace("onclick=\"showPage('court');return false;\"", "href=\"/court-rental.html\"")
home_inner = home_inner.replace("onclick=\"showPage('home');scrollToId('contact');return false;\"", "href=\"#contact\"")
home_inner = re.sub(r'href="#" onclick="showPage\(\'court\'\);return false;"', 'href="/court-rental.html"', home_inner)
home_inner = re.sub(r'href="#" onclick="showPage\(\'home\'\);scrollToId\(\'about\'\);return false;"', 'href="#about"', home_inner)

# ── Fix court content (remove page wrapper, fix internal links) ───────────
court_inner = court_content.replace('<div class="page" id="page-court">', '')
court_inner = court_inner.replace('</div><!-- /page-court -->', '')
court_inner = court_inner.replace("onclick=\"showPage('home');return false;\"", "href=\"/\"")

# ── Build index.html ──────────────────────────────────────────────────────

home_head = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <title>Britton Baptist Church \u2014 Oklahoma City | Walk in the Light</title>
  <meta name="description" content="Britton Baptist Church \u2014 a lighthouse of hope in Oklahoma City since 1941. Sunday worship, youth programs, community outreach, and indoor basketball court rental. 1141 W Britton Rd, OKC 73114.">
  <meta name="keywords" content="Britton Baptist Church, church Oklahoma City, SBC church OKC, Baptist church north OKC, Oklahoma City church, Sunday worship OKC, youth ministry Oklahoma City">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://brittonbaptist.church/">

  <meta property="og:title" content="Britton Baptist Church \u2014 Oklahoma City">
  <meta property="og:description" content="A lighthouse of hope in Oklahoma City. Join us for worship, community, and faith. Indoor basketball court available for rental.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://brittonbaptist.church/">

  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Church",
    "name": "Britton Baptist Church",
    "description": "Southern Baptist church serving Oklahoma City since 1941. Worship services, youth programs, community outreach, and indoor basketball court rental.",
    "url": "https://brittonbaptist.church",
    "telephone": "+1-405-842-3511",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "1141 W Britton Rd",
      "addressLocality": "Oklahoma City",
      "addressRegion": "OK",
      "postalCode": "73114",
      "addressCountry": "US"
    },
    "geo": {
      "@type": "GeoCoordinates",
      "latitude": 35.5659,
      "longitude": -97.5326
    }
  }
  </script>
'''

# Get the fonts and styles from original
fonts_start = content.find('<link rel="preconnect"')
fonts_end = content.find('</style>') + 8
fonts_and_styles = content[fonts_start:fonts_end]

# Remove .page display none/active rules since we don't need them
fonts_and_styles = fonts_and_styles.replace('    .page { display: none; }\n    .page.active { display: block; }\n', '')

index_html = home_head + '\n' + fonts_and_styles + '\n</head>\n<body>\n\n'
index_html += '  ' + nav_home + '\n\n'
index_html += home_inner + '\n\n'

# Add footer
footer_raw = content[content.find('<footer class="site-footer">'):content.find('</footer>') + 9]
index_html += '  ' + footer_raw + '\n\n'

# Add minimal JS (just smooth scroll and mobile menu)
index_html += '''  <script>
    document.querySelectorAll('.nav-menu a').forEach(link => {
      link.addEventListener('click', () => {
        document.getElementById('navMenu').classList.remove('open');
      });
    });
  </script>

</body>
</html>
'''

# ── Build court-rental.html ───────────────────────────────────────────────

court_head = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <title>Basketball Court Rental OKC | Indoor Gym for Rent | Britton Baptist Church</title>
  <meta name="description" content="Rent an indoor basketball court at Britton Baptist Church in Oklahoma City. Full-size hardwood court, $20/hr, online booking, live streaming. Perfect for pickup basketball, team practices, youth leagues, and private events. 1141 W Britton Rd, OKC 73114.">
  <meta name="keywords" content="basketball court rental Oklahoma City, indoor gym rental OKC, rent basketball court near me, pickup basketball Oklahoma City, basketball court for rent OKC, indoor basketball court rental, gym rental north OKC, court rental 73114, Britton Baptist Church gym, hourly court rental OKC, youth basketball OKC, basketball venue rental Oklahoma City, book basketball court online OKC">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://brittonbaptist.church/court-rental.html">

  <meta property="og:title" content="Basketball Court Rental OKC | Britton Baptist Church">
  <meta property="og:description" content="Rent an indoor basketball court in Oklahoma City. $20/hr, online booking, live streaming. Book at Britton Baptist Church.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://brittonbaptist.church/court-rental.html">

  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "SportsActivityLocation",
    "name": "Britton Baptist Church \u2014 Indoor Basketball Court Rental",
    "description": "Rent an indoor basketball court in Oklahoma City at Britton Baptist Church. Full-size hardwood court, $20/hr, online booking via Sked.Earth, live streaming via Pickup.Earth.",
    "url": "https://brittonbaptist.church/court-rental.html",
    "telephone": "+1-405-842-3511",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "1141 W Britton Rd",
      "addressLocality": "Oklahoma City",
      "addressRegion": "OK",
      "postalCode": "73114",
      "addressCountry": "US"
    },
    "geo": {
      "@type": "GeoCoordinates",
      "latitude": 35.5659,
      "longitude": -97.5326
    },
    "sport": "Basketball",
    "amenityFeature": [
      { "@type": "LocationFeatureSpecification", "name": "Indoor Basketball Court" },
      { "@type": "LocationFeatureSpecification", "name": "Hardwood Floor" },
      { "@type": "LocationFeatureSpecification", "name": "Live Streaming" },
      { "@type": "LocationFeatureSpecification", "name": "Online Booking" },
      { "@type": "LocationFeatureSpecification", "name": "Free Parking" }
    ],
    "isAccessibleForFree": false,
    "priceRange": "$20/hr",
    "potentialAction": {
      "@type": "ReserveAction",
      "target": "https://sked.earth/venues/ewuQ5Va2X1bDRvuVkf5n"
    }
  }
  </script>

  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {
        "@type": "Question",
        "name": "Where can I rent an indoor basketball court in Oklahoma City?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Britton Baptist Church at 1141 W Britton Rd in North Oklahoma City offers a full-size indoor basketball court for hourly rental at $20/hour. Book online at sked.earth."
        }
      },
      {
        "@type": "Question",
        "name": "How much does it cost to rent a basketball court at Britton Baptist Church?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Court rental is $20 per hour, bookable in 30-minute increments at $10 per slot. Book online through the Sked.Earth widget on this page."
        }
      },
      {
        "@type": "Question",
        "name": "Do I need to be a church member to rent the court?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "No. The basketball court is open to everyone in the Oklahoma City community. Church membership is not required."
        }
      },
      {
        "@type": "Question",
        "name": "Is there pickup basketball in Oklahoma City?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Yes. Britton Baptist Church hosts pickup basketball sessions in North OKC. Book a session through Sked.Earth or check the schedule for open play times."
        }
      },
      {
        "@type": "Question",
        "name": "Can I live stream my basketball game?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Yes. The court features professional cameras powered by Pickup.Earth. Games can be live streamed and recorded, with footage archived for 30 days."
        }
      }
    ]
  }
  </script>
'''

court_html = court_head + '\n' + fonts_and_styles + '\n</head>\n<body>\n\n'
court_html += '  ' + nav_court + '\n\n'
court_html += court_inner + '\n\n'
court_html += '  ' + footer_raw + '\n\n'

court_html += '''  <script>
    // FAQ toggles
    document.querySelectorAll('.faq-q').forEach(q => {
      q.addEventListener('click', () => {
        const item = q.parentElement;
        const wasOpen = item.classList.contains('open');
        document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('open'));
        if (!wasOpen) item.classList.add('open');
      });
    });
    document.querySelectorAll('.nav-menu a').forEach(link => {
      link.addEventListener('click', () => {
        document.getElementById('navMenu').classList.remove('open');
      });
    });
    // Auto-resize sked.earth iframe
    window.addEventListener("message", function(e) {
      if (e.data && e.data.type === "sked-resize") {
        var f = document.querySelector("iframe[src*=\\'sked.earth\\']");
        if (f) f.style.height = e.data.height + "px";
      }
    });
  </script>

</body>
</html>
'''

# Write files
with open('index.html', 'w') as f:
    f.write(index_html)
print(f"index.html written ({len(index_html)} chars)")

with open('court-rental.html', 'w') as f:
    f.write(court_html)
print(f"court-rental.html written ({len(court_html)} chars)")
