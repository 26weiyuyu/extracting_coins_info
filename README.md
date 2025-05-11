# Crypto Project Metadata Collector

This repo contains Python scripts to extract and compile metadata for cryptocurrency projects from CoinMarketCap. The final goal is to build a structured dataset with official websites, GitHub links, first token trading dates, and social media for each project.

---

## Project Workflow

1. **Scrape CoinMarketCap Coin List**  
   📄 `scrape_coin_list.py`  
   - Extracts coin names and their CoinMarketCap links.
   - Saves to: `your output file`

2. **Get First Token Trading Date**  
   📄 `scrape_token_dates.py`  
   - Uses Selenium to hover over CoinMarketCap charts and find the first date with price data.
   - Saves to: `your output file`

3. **Extract Website and Social Links**  
   📄 `extract_all_links.py`  
   - Extracts and classifies all links on each coin’s page: GitHub, official website, Twitter, Reddit, etc.
   - Saves to: `your output file`

4. **Merge Metadata with OSS Info**  
   📄 `merge_project_data.py`  
   - Combines token dates, CoinMarketCap metadata, and GitHub OSS links into one final file.
   - Saves to: `your output file`

---

## 📁 Example Output Columns

| Column              | Description                                 |
|---------------------|---------------------------------------------|
| Coin                | Project name (from CMC)                     |
| Link                | CoinMarketCap URL                           |
| First Token Date    | First trading day from chart                |
| GitHub Link         | Detected GitHub repo URL                    |
| Official Website    | Main project website                        |
| Twitter Link        | Twitter profile                             |
| Reddit Link         | Reddit community                            |
| White Paper Link    | PDF or Google Doc whitepaper                |
| Explorer            | Blockchain explorer                         |
| Other               | Uncategorized additional links              |

---

## Setup

### Required Packages:
- `pandas`
- `requests`
- `beautifulsoup4`
- `selenium`

Install with:
```bash
pip install -r requirements.txt
