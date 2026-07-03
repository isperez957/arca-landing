# Arca AI — Landing Page

**AI for Private Capital.** Arca AI gives family offices, hedge funds, and private banks an intelligence layer that automates research, compliance, and deal sourcing.

## Overview

Single-page landing site built with vanilla HTML, CSS, and JavaScript. No frameworks, no build step — open `index.html` in any browser.

### Features

- **Trilingual** — English, Spanish (ES), and French (FR) with language toggle
- **Dark theme** — Custom purple/cyan/green palette with animated background
- **Responsive** — Works on desktop and mobile
- **Inline SVG** — Animated AI network visualization (hero section)
- **Scroll reveal** — Intersection Observer for fade-in animations
- **Contact form** — Demo request form + direct email/phone

### Sections

- Hero with animated AI graph
- Problem vs. Solution comparison
- Feature cards (AI Research, Compliance, Deal Sourcing, Stress Testing, etc.)
- How it works (4-step timeline)
- Stats bar
- Testimonials
- Pricing (Starter / Professional / Enterprise)
- Contact form + direct contact info

## Quick Start

```bash
# Clone
git clone https://github.com/isperez957/arca-landing.git
cd arca-landing

# Open in browser
xdg-open index.html

# Or with the arca-browser helper (app-mode window, no chrome)
arca-browser file://$(pwd)/index.html
```

## Pricing

| Plan         | Price         | Audience                        |
|-------------|---------------|----------------------------------|
| Starter     | €3,400/mo     | Single-family office            |
| Professional| €9,999/mo     | Multi-family office / Hedge fund |
| Enterprise  | Custom        | Private bank / Institution       |

## Structure

```
arca-landing/
├── index.html       # Everything — HTML, CSS, JS, SVG inline
├── lambda/          # Contact form handler (Python)
│   └── submit-contact.py
├── .github/
│   └── workflows/   # CI/CD: S3 sync + CloudFront invalidation
└── README.md
```

## Infrastructure

IaC managed in the consolidated [terraform](https://github.com/isperez957/terraform) repo (`landing-web/` folder).

| Resource | Detail |
|---|---|
| S3 | `arca-landing-649091762015` (static hosting) |
| CloudFront | `ES3RSFQ2A0Q1O` (CDN, PriceClass_100) |
| Lambda | `arca-submit-contact` (Python 3.12, Function URL) |

## Contact

- **Email:** isaacpe@gmail.com
- **Phone:** +34 609 01 02 57
- **Repo:** https://github.com/isperez957/arca-landing

## License

Private — all rights reserved.
