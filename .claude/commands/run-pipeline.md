---
name: run-pipeline
description: Run the daily trending pipeline with various options
---

# Run Pipeline

Execute the daily trending data collection and website generation pipeline.

## Input - Use AskUserQuestion Tool

### Required: Run Mode
**Use AskUserQuestion with these parameters:**
```
question: "How should I run the pipeline?"
header: "Mode"
multiSelect: false
options:
  - label: "Full run (Recommended)"
    description: "Complete pipeline with archiving"
  - label: "No archive"
    description: "Skip archiving previous data"
  - label: "Dry run"
    description: "Validate without generating output"
  - label: "Debug mode"
    description: "Verbose logging for troubleshooting"
```

### Optional: Pipeline Steps
**Use AskUserQuestion with these parameters:**
```
question: "Which steps should I run?"
header: "Steps"
multiSelect: true
options:
  - label: "All steps"
    description: "Run complete 14-step pipeline"
  - label: "Collect only"
    description: "Only fetch trends from sources"
  - label: "Build only"
    description: "Build HTML from existing data"
  - label: "Images only"
    description: "Fetch/refresh images for trends"
```

## CLI Alternative

```bash
/run-pipeline                  # Full pipeline run
/run-pipeline --no-archive     # Skip archiving
/run-pipeline --dry-run        # Validation only
```

## Commands

### Full Pipeline
```bash
cd scripts && python main.py
```

### No Archive
```bash
cd scripts && python main.py --no-archive
```

### Dry Run
```bash
cd scripts && python main.py --dry-run
```

## Pipeline Steps (14 total)

1. Archive previous data
2. Collect trends (12 sources)
3. Fetch images
4. Enrich content
5. Load yesterday's data
6. Generate AI design
7. Generate editorial articles
8. Generate topic pages
9. Build HTML
10. Generate RSS
11. Generate PWA files
12. Generate sitemap
13. Cleanup
14. Save data

## Quality Gates

- **MIN_TRENDS = 5**: Abort if fewer than 5 trends collected
- **MIN_FRESH_RATIO = 0.5**: Warn if less than 50% fresh in 24h

## Troubleshooting

| Issue | Solution |
|-------|----------|
| API rate limits | Check GROQ_API_KEY, use OPENROUTER_API_KEY backup |
| Missing images | Verify PEXELS_API_KEY, UNSPLASH_ACCESS_KEY |
| Low trend count | Check source availability, increase LIMITS in config.py |
