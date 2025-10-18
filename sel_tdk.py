import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# Setup headless Chrome
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=options)

# Load Excel file
df = pd.read_excel("tdk_list_jp.xlsx")

# Create result columns
df["Actual Title"] = ""
df["Actual Keyword"] = ""
df["Actual Description"] = ""
df["Title Match"] = ""
df["Keyword Match"] = ""
df["Description Match"] = ""

for i, row in df.iterrows():
    try:
        base_url = "http://staging.hiwork.jp:3000/"
        full_url = base_url + row["URL"].lstrip("/")  # Clean extra slashes

        driver.get(full_url)
        time.sleep(1.5)  # Wait for JS to render (adjust if needed)

        # Extract title and meta content
        actual_title = driver.title.strip()
        actual_keyword = driver.execute_script("return document.querySelector('meta[name=keyword]')?.content || ''").strip()
        actual_desc = driver.execute_script("return document.querySelector('meta[name=description]')?.content || ''").strip()

        df.at[i, "Actual Title"] = actual_title
        df.at[i, "Actual Keyword"] = actual_keyword
        df.at[i, "Actual Description"] = actual_desc
        df.at[i, "Title Match"] = actual_title == str(row["Expected Title"]).strip()
        df.at[i, "Keyword Match"] = actual_keyword == str(row["Expected Keyword"]).strip()
        df.at[i, "Description Match"] = actual_desc == str(row["Expected Description"]).strip()

    except Exception as e:
        df.at[i, "Actual Title"] = f"Error: {e}"
        df.at[i, "Actual Keyword"] = f"Error: {e}"
        df.at[i, "Actual Description"] = f"Error: {e}"

driver.quit()

# Save result
df.to_excel("tdk_check_results_jp.xlsx", index=False)
print("✅ TDK check completed. Results saved to 'tdk_check_results_jp.xlsx'")
