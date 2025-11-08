# dueDilligence

**AI-Powered Land Due Diligence Platform**

An intelligent automation platform for land investment research and analysis, combining data acquisition, processing, and AI-driven insights.

## 🎯 Vision

Transform land due diligence from a manual, time-consuming process into an automated, AI-powered workflow that provides comprehensive insights for informed investment decisions.

## 🏗️ Project Structure

```
dueDilligence/
├── scrapers/          # Data Acquisition
│   └── mohave/        # Mohave County scraper
├── data/              # Data Storage
│   ├── raw/           # Raw scraped data
│   └── processed/     # Cleaned data (future)
├── analysis/          # AI Analysis (future)
├── utils/             # Shared utilities
├── docs/              # Documentation
└── tests/             # Testing suite
```

## 🚀 Current Features

### Data Acquisition
- **Mohave County Scraper**: Automated scraping of property sales data
  - 55,000+ vacant land records collected
  - Full pagination support
  - Date range: 01/01/2010 to 10/31/2025
  - See [scrapers/mohave/README.md](scrapers/mohave/README.md)

## 🔮 Planned Features

### AI Analysis (Coming Soon)
- Market trend analysis and predictions
- Automated risk assessment
- Comparable property analysis
- Investment scoring and recommendations
- Natural language due diligence reports

### Additional Data Sources
- Multiple county assessor websites
- Public land records
- Market data integration
- Environmental data

## 📊 Quick Start

### Prerequisites
- Python 3.8+
- Chrome/Chromium browser

### Installation

```bash
# Clone the repository
git clone https://github.com/pubuduyashan/dueDilligence.git
cd dueDilligence

# Install dependencies
pip install -r requirements.txt
```

### Run Mohave County Scraper

```bash
# Test with 3 books
cd scrapers/mohave
python test_scraper.py

# Run full scraper (311 books)
python scraper.py
```

Data will be saved to `data/raw/mohave/`

## 📁 Data

Current dataset: **55,072 vacant land sales records** from Mohave County

Each record includes:
- Sale Parcel ID
- Associated Parcels
- Property Type
- Reception Number
- Sale Price
- Sale Date
- Book Number
- Timestamp

## 🛠️ Tech Stack

- **Python 3.12**
- **Selenium**: Web automation
- **BeautifulSoup4**: HTML parsing
- **Pandas**: Data processing
- **Future**: AI/ML frameworks for analysis

## 📖 Documentation

- [Scraper Guide](docs/scraper_guide.md) - Detailed scraping documentation
- [Data Structure](data/README.md) - Data organization
- [Analysis Module](analysis/README.md) - AI features (coming soon)

## 🤝 Contributing

This project is under active development. More modules and features coming soon!

## 📝 License

For educational and authorized use only.

---

**🤖 Built with AI assistance from [Claude Code](https://claude.com/claude-code)**
