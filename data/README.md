# Data Directory

This directory contains all project data organized by processing stage.

## Structure

```
data/
├── raw/              # Raw scraped data (unmodified)
│   └── mohave/       # Mohave County data
└── processed/        # Cleaned and processed data (future)
```

## Raw Data
Contains unprocessed data directly from scrapers.
- **Format**: CSV files
- **Source**: County assessor websites
- **Do not modify**: These are source-of-truth records

## Processed Data (Future)
Will contain cleaned, validated, and enriched data ready for analysis.
