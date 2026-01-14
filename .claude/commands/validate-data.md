---
name: validate-data
description: Validate data integrity and quality for the trending pipeline
---

# Validate Data

Check data files, cache integrity, and content quality.

## Input - Use AskUserQuestion Tool

### Required: Validation Scope
**Use AskUserQuestion with these parameters:**
```
question: "What should I validate?"
header: "Scope"
multiSelect: true
options:
  - label: "All (Recommended)"
    description: "Full validation of all data files"
  - label: "Trends data"
    description: "Validate trends.json structure and content"
  - label: "Image cache"
    description: "Check image cache integrity and expiry"
  - label: "Output files"
    description: "Validate generated HTML, RSS, sitemap"
  - label: "Archive"
    description: "Check archive integrity and completeness"
```

### Optional: Validation Depth
**Use AskUserQuestion with these parameters:**
```
question: "How thorough should validation be?"
header: "Depth"
multiSelect: false
options:
  - label: "Quick check"
    description: "File existence and basic structure"
  - label: "Standard"
    description: "Structure, content, and references"
  - label: "Deep scan"
    description: "Full content analysis with URL checks"
```

## CLI Alternative

```bash
/validate-data                 # Validate all data
/validate-data trends          # Trends only
/validate-data images          # Image cache only
```

## Validation Checks

### Trends Data (`data/trends.json`)
```bash
# Check file exists and is valid JSON
python -c "import json; json.load(open('data/trends.json'))"

# Check trend count
python -c "import json; d=json.load(open('data/trends.json')); print(f'{len(d)} trends')"
```

### Image Cache (`data/image_cache/`)
```bash
# Check cache age (7-day TTL)
find data/image_cache -type f -mtime +7 -ls

# Count cached images
ls -1 data/image_cache/*.json 2>/dev/null | wc -l
```

### Output Files
```bash
# Check required files exist
ls -la public/index.html public/feed.xml public/sitemap.xml

# Validate HTML
python -c "from html.parser import HTMLParser; HTMLParser().feed(open('public/index.html').read())"
```

### Archive Integrity
```bash
# Count archive entries (30-day retention)
ls -1 public/archive/ 2>/dev/null | wc -l

# Check oldest/newest
ls -lt public/archive/ | head -5
ls -lt public/archive/ | tail -5
```

## Quality Metrics

| Metric | Threshold | Check |
|--------|-----------|-------|
| Trend count | >= 5 | MIN_TRENDS |
| Fresh ratio | >= 50% | MIN_FRESH_RATIO |
| Image coverage | >= 80% | Trends with images |
| Archive days | <= 30 | ARCHIVE_KEEP_DAYS |
| Cache age | <= 7 days | IMAGE_CACHE_MAX_AGE_DAYS |
