# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DailyTrending.info is a fully autonomous trend aggregation website that regenerates daily at 6 AM EST via GitHub Actions. It collects English-only content from 12+ sources, generates unique AI-driven designs (~50M combinations), and deploys to GitHub Pages at zero cost.

**Live Site:** https://dailytrending.info

## Build & Development Commands

```bash
# Run full pipeline (from scripts/ directory)
cd scripts && python main.py

# Skip archiving previous site
python main.py --no-archive

# Dry run (collect data, generate design, but don't build HTML)
python main.py --dry-run

# Run tests
pytest tests/

# Run tests with coverage
pytest tests/ --cov=scripts

# Run a single test file
pytest tests/test_design_system.py

# Run specific test
pytest tests/test_design_system.py::test_design_spec_creation -v
```

## Environment Variables

Required secrets (in `.env` locally or GitHub Secrets for CI):
- `GROQ_API_KEY` - Primary AI for design generation (recommended)
- `OPENROUTER_API_KEY` - Backup AI option
- `PEXELS_API_KEY` - Primary image source
- `UNSPLASH_ACCESS_KEY` - Backup image source

## Architecture

### Pipeline Flow (14 steps in `main.py`)

1. Archive previous site → 2. Collect trends (12 sources) → 3. Fetch images → 4. Enrich content (Word of Day, Grokipedia) → 5. Load yesterday's trends (for comparison) → 6. Generate AI design → 7. Generate editorial article → 8. Generate topic pages (/tech, /world, /social) → 9. Build HTML/CSS/JS → 10. Generate RSS (with content:encoded) → 11. Generate PWA assets → 12. Generate sitemap (includes articles) → 13. Cleanup old archives → 14. Save pipeline data

### Key Modules (`scripts/`)

| Module | Purpose |
|--------|---------|
| `main.py` | Pipeline orchestrator with quality gates |
| `collect_trends.py` | 12-source aggregator with deduplication |
| `fetch_images.py` | Pexels/Unsplash with 7-day persistent cache |
| `generate_design.py` | 9 personalities, 20+ color schemes, 12 hero styles |
| `build_website.py` | Single-file HTML/CSS/JS builder (largest file) |
| `enrich_content.py` | AI-generated Word of Day, Grokipedia articles |
| `editorial_generator.py` | Daily editorial articles with structured 8-section format |
| `generate_rss.py` | RSS 2.0 with content:encoded and Dublin Core |
| `sitemap_generator.py` | XML sitemap with articles and topic pages |
| `config.py` | All magic numbers, timeouts, limits |
| `archive_manager.py` | 30-day dated snapshots |

### Data Flow

```
12 Sources → trends.json → images.json → design.json → public/index.html
                              ↓
                      data/image_cache/ (7-day TTL)
```

### Output Structure

All output goes to `public/`:
- `index.html` - Self-contained single-file site (inline CSS/JS)
- `feed.xml` - RSS feed with content:encoded
- `sitemap.xml` - SEO sitemap (includes articles and topic pages)
- `manifest.json` + `sw.js` - PWA assets
- `archive/` - 30-day historical snapshots
- `articles/` - Permanently retained editorial articles
  - `index.html` - Articles listing page
  - `YYYY/MM/DD/slug/` - Individual article pages with metadata.json
- `tech/index.html` - Technology-focused topic page
- `world/index.html` - World news topic page
- `social/index.html` - Viral/social trends topic page

## Quality Gates

The pipeline enforces two quality gates in `_step_collect_trends()`:
- **MIN_TRENDS = 5** - Aborts if fewer than 5 trends collected
- **MIN_FRESH_RATIO = 0.5** - Warns if <50% of trends are from past 24h

## Design System

9 personalities (brutalist, editorial, minimal, corporate, playful, tech, news, magazine, dashboard) each have aligned:
- Hero styles (12 options: cinematic, glassmorphism, neon, particles, etc.)
- Typography scales (different heading ratios)
- Animation levels (none → energetic)
- Color schemes (20+ options)

Design selection is AI-driven (Groq) or falls back to preset themes.

## Editorial Articles

The `editorial_generator.py` module creates daily editorial articles that synthesize top stories into cohesive narratives.

### Article Structure (8 Required Sections)
1. **The Lead** - Hook with surprising insight + thesis
2. **What People Think** - Steelman conventional wisdom
3. **What's Actually Happening** - Contrarian/deeper analysis with evidence
4. **The Hidden Tradeoffs** - Unspoken costs and trade-offs
5. **The Best Counterarguments** - Steelman strongest objection
6. **What This Means Next** - Concrete predictions with timeframes
7. **Practical Framework** - Actionable mental model
8. **Conclusion** - Circle back to hook

### Key Features
- Articles permanently retained (not archived like daily snapshots)
- URL structure: `/articles/YYYY/MM/DD/slug/`
- Includes JSON-LD structured data for SEO
- "Why This Matters" context for top 3 stories
- Central theme identification from keyword frequency analysis

### Editing the Prompt Template
The editorial prompt is in `editorial_generator.py::generate_editorial()`. It uses:
- `_build_editorial_context()` for story summaries
- `_identify_central_themes()` for thesis question generation

## User Features

### Saved Stories (localStorage)
Users can save stories via bookmark buttons. Saved stories persist in browser localStorage:
- `dailytrending_saved` - Array of saved story objects
- No backend required - fully client-side
- Saved stories panel in the UI

### Topic Sub-Pages
Filtered views by source category:
- `/tech/` - HackerNews, Lobsters, GitHub Trending, tech RSS
- `/world/` - News RSS, Wikipedia current events
- `/social/` - Reddit, viral content

## RSS Feed

Enhanced RSS 2.0 with:
- `content:encoded` - Full HTML content per item
- `dc:creator` - Dublin Core author attribution
- "Why This Matters" context when available
- Atom self-link for feed validation

## Trending Indicators

### Velocity Badges
Stories display velocity indicators based on cross-source mentions:
- **HOT** (red) - 80+ score, appears in 4+ sources
- **RISING** (yellow) - 50-79 score, appears in 2-3 sources
- **STEADY** (accent) - 30-49 score, established trend
- (no badge) - New/single-source stories

Calculated in `_calculate_velocity()` based on keyword overlap between stories.

### Compare to Yesterday
Visual indicators showing trend status:
- 🆕 **New today** - First appearance
- 🔥 **Trending up** - Similar story from yesterday, still active
- 📊 **Continuing** - Exact URL match from yesterday

Calculated in `_get_comparison_indicator()` using fuzzy title matching.

## Reading Time

Total reading time displayed in section headers:
- Calculated at 200 WPM average
- `_calculate_reading_time()` and `_get_total_reading_time()` methods
- Shows in "Top Stories" section header

## Social Sharing

Native Web Share API integration with fallback:
1. Uses `navigator.share()` on supported devices (mobile, modern browsers)
2. Falls back to clipboard copy with toast notification
3. Final fallback: prompt dialog

Share buttons appear on hover over story cards.

## Accessibility

### Implemented Features
- **Skip link** - "Skip to main content" for keyboard users
- **Focus visible** - Clear focus indicators for keyboard navigation
- **ARIA labels** - Descriptive labels on interactive elements
- **Screen reader support** - Live region for dynamic announcements
- **Keyboard navigation** - Arrow keys to navigate between story cards
- **Reduced motion** - Respects `prefers-reduced-motion`
- **High contrast** - Adapts to `prefers-contrast: high`

### Keyboard Shortcuts
- `↑/↓` or `←/→` - Navigate between story cards
- `Enter` - Open focused story in new tab
- `Escape` - Remove focus

## LLM-Optimized SEO

### Enhanced JSON-LD Schemas
The `_build_structured_data()` method generates:
- `WebSite` - Basic site info
- `WebPage` - Page metadata with breadcrumbs
- `ItemList` - Top 10 trending stories
- `FAQPage` - Common questions answered
- `HowTo` - Site usage guide (4 steps)
- `SpeakableSpecification` - Voice assistant optimization
- `Article` with `mentions` - Entity linking for LLM understanding

### Speakable Content
CSS selectors marked as speakable for voice assistants:
- `.headline-xl` - Main headline
- `.hero-subheadline` - Subheadline
- `.story-title` - Individual story titles

## Testing Notes

- Tests use fixtures from `tests/conftest.py` (sample_trends, sample_images, sample_design)
- External APIs are mocked; no real API calls in tests
- `test_design_system.py` has extensive design validation coverage
- Run from project root, not from `tests/` directory

## GitHub Actions Workflows

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `daily-regenerate.yml` | Daily 6 AM EST, push to main, manual | Main build pipeline |
| `auto-merge-claude.yml` | Push to `claude/**` branches | Auto-create and merge PRs |
| `update-readme.yml` | Push to main | Auto-update changelog |

## Common Patterns

**Converting dataclasses to dicts for JSON/templates:**
```python
from dataclasses import asdict
trends_data = [asdict(t) if hasattr(t, '__dataclass_fields__') else t for t in self.trends]
```

**Font whitelist in `config.py`:**
All fonts must be in `ALLOWED_FONTS` to prevent injection attacks.

**Image fallbacks:**
When APIs fail: persistent cache → gradient placeholders

## Configuration Reference (`config.py`)

Key settings to know:
- `LIMITS` dict - Per-source fetch limits
- `TIMEOUTS` dict - HTTP timeouts by operation type
- `DELAYS` dict - Rate limiting between requests
- `IMAGE_CACHE_MAX_AGE_DAYS = 7`
- `ARCHIVE_KEEP_DAYS = 30`
- `DEDUP_SIMILARITY_THRESHOLD = 0.8`
