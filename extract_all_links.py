import os
import sys
import signal
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# === User-configurable ===
input_file        = "Your input file path"
output_file       = "Your output file path"
checkpoint_every  = 1
headless          = True
# =========================

# ——— Read or resume —
if os.path.exists(output_file):
    df = pd.read_csv(output_file)
    start_idx = df["GitHub Link"].isna().idxmax()
    print(f"Resuming at index {start_idx}")
else:
    df = pd.read_csv(input_file)
    for col in ["Official Website", "GitHub Link", "White Paper Link", "Explorer",
                "Twitter Link", "Discord Link", "Reddit Link", "Telegram Link", "Facebook Link", "Other"]:
        if col not in df.columns:
            df[col] = pd.NA
    start_idx = 0

# ——— Chrome setup ——
options = Options()
if headless:
    options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

def save_and_exit(sig, frame):
    print(f"\nSignal {sig} received — saving progress to {output_file} …")
    df.to_csv(output_file, index=False)
    driver.quit()
    sys.exit(0)

# catch Ctrl+C
signal.signal(signal.SIGINT, save_and_exit)

# ——— Set of keywords to exclude from official website classification
exclude_keywords = [
    "coinmarketcap.com", "github.com", "twitter.com", "discord", "reddit.com",
    "t.me", "telegram", "facebook.com", "whitepaper", "explorer", "youtube.com", "instagram.com", "medium.com"
]

try:
    for i in range(start_idx, len(df)):
        slug = df.at[i, "Link"]
        if pd.isna(slug):
            continue

        url = f"https://coinmarketcap.com{slug}"
        print(f"[{i+1}/{len(df)}] → {url}", end=" … ")
        driver.get(url)

        try:
            links_section = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class, 'content')]")
            ))
            all_links = links_section.find_elements(By.TAG_NAME, "a")

            for link in all_links:
                href = link.get_attribute("href")
                if not href or not href.startswith("http"):
                    continue
                href_lower = href.lower()

                if "github.com" in href_lower:
                    df.at[i, "GitHub Link"] = href
                elif "whitepaper" in href_lower or "docs.google.com" in href_lower:
                    df.at[i, "White Paper Link"] = href
                elif "explorer" in href_lower:
                    df.at[i, "Explorer"] = href
                elif "twitter.com" in href_lower:
                    df.at[i, "Twitter Link"] = href
                elif "discord" in href_lower:
                    df.at[i, "Discord Link"] = href
                elif "reddit.com" in href_lower:
                    df.at[i, "Reddit Link"] = href
                elif "t.me" in href_lower or "telegram" in href_lower:
                    df.at[i, "Telegram Link"] = href
                elif "facebook.com" in href_lower:
                    df.at[i, "Facebook Link"] = href
                elif not any(keyword in href_lower for keyword in exclude_keywords):
                    # Assign as official website if it hasn't been filled yet
                    if pd.isna(df.at[i, "Official Website"]):
                        df.at[i, "Official Website"] = href
                    else:
                        df.at[i, "Other"] = str(df.at[i, "Other"]) + ", " + href
                else:
                    # All other links fall to "Other"
                    df.at[i, "Other"] = str(df.at[i, "Other"]) + ", " + href if pd.notna(df.at[i, "Other"]) else href

        except Exception as e:
            print(f"  → Error: {e}")
        print("✓")

        if (i - start_idx + 1) % checkpoint_every == 0:
            df.to_csv(output_file, index=False)
            print(f"  → checkpoint saved at index {i}")

finally:
    print("Run complete (or aborted). Final save …")
    df.to_csv(output_file, index=False)
    driver.quit()
