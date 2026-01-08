# Security Workflow Setup Guide

## Overview

To implement automated dependency scanning in the CI/CD pipeline, create a GitHub Actions workflow file.

## Manual Setup Instructions

Create `.github/workflows/security.yml` with the following content:

```yaml
name: Security Scan

on:
  pull_request:
    branches: [ main ]
  push:
    branches: [ main ]
  schedule:
    - cron: '0 9 * * 1'  # Weekly on Monday 9 AM UTC
  workflow_dispatch:

permissions:
  contents: read
  security-events: write

jobs:
  security-scan:
    name: Dependency Security Scan
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pip-audit safety

      - name: Run pip-audit
        run: pip-audit --desc

      - name: Run safety check
        run: safety check
```

## What This Workflow Does

1. **Automated Scanning**: Runs on every PR, push to main, and weekly
2. **Vulnerability Detection**: Uses pip-audit and safety to find known vulnerabilities
3. **Dependency Analysis**: Checks all Python dependencies for security issues

## Benefits

- Early vulnerability detection
- Automated security updates
- Compliance with security best practices
- Weekly scans catch new vulnerabilities

## Next Steps

After creating the workflow:
1. Commit and push to your repository
2. Check the Actions tab to verify it runs
3. Review any security findings
4. Set up automated PR comments for vulnerability reports (optional)
