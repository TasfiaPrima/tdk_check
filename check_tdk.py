import pandas as pd
import requests
from bs4 import BeautifulSoup

# Load Excel file
df = pd.read_excel("tdk_list.xlsx")

# Create result columns
df["Actual Title"] = ""
df["Actual Keyword"] = ""
df["Actual Description"] = ""
df["Title Match"] = ""
df["Keyword Match"] = ""
df["Description Match"] = ""

for i, row in df.iterrows():
    try:
        base_url = "http://staging.hiwork.jp:3000/en"

        full_url = base_url + row["URL"]  # Concatenates 'https://hiwork.jp' + '/login/'

        response = requests.get(full_url, timeout=10)
        #response = requests.get(row["URL"], timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        
        actual_title = soup.title.string.strip() if soup.title else ""
        key_tag = soup.find("meta", attrs={"name": "keyword"})
        actual_keyword = key_tag["content"].strip() if key_tag else ""
        desc_tag = soup.find("meta", attrs={"name": "description"})
        actual_desc = desc_tag["content"].strip() if desc_tag else ""

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

# Save result
df.to_excel("tdk_check_results.xlsx", index=False)
print("✅ Check completed. Results saved to 'tdk_check_results.xlsx'")
