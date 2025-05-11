# Crypto Project Metadata Collector

This repository contains a suite of Python scripts for scraping, classifying, and merging metadata about cryptocurrency projects from CoinMarketCap. The goal is to build a structured dataset including project links, GitHub repositories, and first token trading dates, to support deeper analysis of open-source crypto ecosystems with github activities and different funding models. 

---

## Project Workflow

1. **Scrape CoinMarketCap Coin List**  
   `scrape_coin_list.py`  
   - Extracts coin names and their CoinMarketCap links.
   - Saves to: `your output file`

2. **Get First Token Trading Date**  
   `scrape_token_dates.py`  
   - Uses Selenium to hover over CoinMarketCap charts and find the first date with price data.
   - Saves to: `your output file`

3. **Extract Website and Social Links**  
   `extract_all_links.py`  
   - Extracts all available external links from each coin’s CoinMarketCap page (website, GitHub, whitepaper, explorers, etc.).
   - Saves to: `your output file`

4. **Merge Metadata with OSS Info**  
   `merge_project_data.py`  
   - Combines token dates, CoinMarketCap metadata, and GitHub OSS links into one final file.
   - Saves to: `your output file`

---

## Example Output Columns

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
```
---

## Notes

- For heavy scraping (over hundreds of coins), you may want to add random sleep intervals and use checkpoint saving to avoid losing progress.
- Coin names may not always match OSS GitHub repositories directly, so link classification is essential.
- Selenium scripts can be resource-intensive; ensure ChromeDriver is up-to-date.
