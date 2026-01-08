---
name: test-sources
description: Test individual trend sources for availability and data quality
---

# Test Sources

Test connectivity and data quality for individual trend sources.

## Input - Use AskUserQuestion Tool

### Required: Source Selection
**Use AskUserQuestion with these parameters:**
```
question: "Which sources should I test?"
header: "Sources"
multiSelect: true
options:
  - label: "All sources (Recommended)"
    description: "Test all 12 trend sources"
  - label: "Tech sources"
    description: "HackerNews, Lobsters, GitHub, ProductHunt"
  - label: "News sources"
    description: "RSS feeds, Wikipedia, news APIs"
  - label: "Social sources"
    description: "Reddit, viral content sources"
```

### Optional: Test Mode
**Use AskUserQuestion with these parameters:**
```
question: "What type of test?"
header: "Mode"
multiSelect: false
options:
  - label: "Connectivity"
    description: "Just check if sources respond"
  - label: "Data quality"
    description: "Fetch sample data and validate"
  - label: "Full test"
    description: "Complete fetch with deduplication"
```

## CLI Alternative

```bash
/test-sources                  # Test all sources
/test-sources tech             # Tech sources only
/test-sources --quick          # Connectivity only
```

## Source List (12 total)

| Source | Category | Check |
|--------|----------|-------|
| HackerNews | Tech | API status |
| Lobsters | Tech | RSS feed |
| GitHub Trending | Tech | HTML scrape |
| ProductHunt | Tech | API/scrape |
| Reddit | Social | API status |
| Wikipedia | News | API status |
| RSS Feeds | News | Multiple feeds |
| Viral content | Social | Various |

## Test Commands

### Quick connectivity test
```bash
cd scripts && python -c "
from collect_trends import *
import asyncio

async def test():
    # Test each source
    sources = ['hackernews', 'lobsters', 'github', 'reddit']
    for s in sources:
        try:
            print(f'Testing {s}...')
            # Add source-specific test
        except Exception as e:
            print(f'{s}: FAILED - {e}')

asyncio.run(test())
"
```

### Full source test
```bash
pytest tests/test_collect_trends.py -v
```

## Troubleshooting

| Source | Common Issues | Solution |
|--------|---------------|----------|
| HackerNews | Rate limited | Increase DELAYS.hackernews |
| GitHub | HTML changes | Update scraper selectors |
| Reddit | API blocked | Check user agent, rate limits |
| RSS | Feed unavailable | Try backup feeds |
