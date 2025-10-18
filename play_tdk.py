import pandas as pd
from playwright.sync_api import sync_playwright

# Load Excel
df = pd.read_excel("c_tdk.xlsx")
df["Actual Title"] = ""
df["Actual Keyword"] = ""
df["Actual Description"] = ""
df["Title Match"] = ""
df["Keyword Match"] = ""
df["Description Match"] = ""

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    for i, row in df.iterrows():
        try:
            base_url = "https://hiwork.jp/en/client"
            full_url = base_url + row["URL"].lstrip("/")

            print(f"[{i+1}/{len(df)}] Checking: {full_url}")
            page.goto(full_url, timeout=10000)

            actual_title = page.title()
            actual_keyword = page.locator("meta[name='keyword']").get_attribute("content") or ""
            actual_desc = page.locator("meta[name='description']").get_attribute("content") or ""

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

    browser.close()

# Save output
df.to_excel("tdk_check_results_playwright_c.xlsx", index=False)
print("✅ TDK check completed using Playwright.")
