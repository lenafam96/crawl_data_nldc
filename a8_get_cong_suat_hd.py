import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
import logging

# ==============================================================================
# LOGGING CONFIGURATION (Writes logs to log.txt instead of the terminal)
# ==============================================================================
logging.basicConfig(
    filename='z9_temp_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d/%m/%Y %H:%M:%S',
    encoding='utf-8'
)

# ==============================================================================
# INTEGRATED FUNCTIONS (Standalone requests functions)
# ==============================================================================

def cong_suat_hd(day, month, year):
    url = f"https://www.nsmo.vn/HTDCongSuatHD?day={day}%2F{month}%2F{year}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()
    return response.text

def thong_so_vh(day, month, year):
    url = f"https://www.nsmo.vn/HTDThongSoVH?day={day}%2F{month}%2F{year}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()
    return response.text

# ==============================================================================
# MAIN CRAWLER LOGIC
# ==============================================================================

# 1. Config your date range using 'dd/mm/yyyy' string format here
start_date_str = "21/10/2025"
end_date_str = "21/10/2025"  # Change this to crawl more days

# Convert input strings to native datetime objects safely
start_date = datetime.strptime(start_date_str, "%d/%m/%Y")
end_date = datetime.strptime(end_date_str, "%d/%m/%Y")

# Fixed categories in the exact order they appear on the website
categories = [
    "Quốc gia + ĐMT mái nhà (ước tính thương phẩm)",
    "Quốc gia + ĐMT mái nhà (ước tính đầu cực)",
    "Thủy điện",
    "Nhiệt điện than",
    "Tuabin khí (Gas + Dầu DO)",
    "Nhiệt điện dầu",
    "Điện gió",
    "ĐMT trang trại",
    "ĐMT mái nhà (ước tính thương phẩm)",
    "ĐMT mái nhà (ước tính đầu cực)",
    "Nhập khẩu điện",
    "Khác (Sinh khối, Diesel Nam, …)"
]

# Create standard columns for the final Excel sheet layout
excel_columns = ["Ngày", "Mục"] + categories

# Array to store all structured rows across the entire date range
all_excel_rows = []

# Log the starting process instead of printing to terminal
logging.info("Starting to crawl data...")

# 2. Loop through each day in the date range
while start_date <= end_date:
    day = start_date.strftime("%d")
    month = start_date.strftime("%m")
    year = start_date.strftime("%Y")
    date_str = f"{day}/{month}/{year}"

    # TRY/EXCEPT BLOCK: Protects against network disconnections or empty pages for any specific day
    try:
        # Fetch the raw HTML source code using the integrated standard requests function
        html_raw = cong_suat_hd(day, month, year)
        
        # Explicitly declare 'html.parser' to parse the HTML string safely
        soup = BeautifulSoup(html_raw, "html.parser")
        
        # Extract all raw text from the page to process with regex pattern matching
        web_text = soup.get_text()

        # Temporary lists to store peak values for the current day
        noon_values = []
        evening_values = []

        # Use regular expressions to separate noon and evening numbers for each category
        for i, cat in enumerate(categories):
            next_cat = categories[i+1] if i + 1 < len(categories) else "$"
            pattern = re.escape(cat) + r"(.*?)(?=" + re.escape(next_cat) + r"|$)"
            match = re.search(pattern, web_text, re.DOTALL)
            
            if match:
                data_part = match.group(1).strip()
                # Find all numbers (including decimal numbers that use commas)
                numbers = re.findall(r"\d+,\d+|\d+", data_part)
                
                if len(numbers) >= 2:
                    # Convert commas ',' to dots '.' so Excel recognizes them as real Float values
                    noon_values.append(float(numbers[0].replace(",", ".")))
                    evening_values.append(float(numbers[1].replace(",", ".")))
                elif len(numbers) == 1 and (numbers[0] == "00" or numbers[0] == "0"):
                    noon_values.append(0.0)
                    evening_values.append(0.0)
                else:
                    noon_values.append(0.0)
                    evening_values.append(0.0)
            else:
                noon_values.append(0.0)
                evening_values.append(0.0)

        # If the day contains data or the key term is found, append it to the master rows list
        if any(noon_values) or any(evening_values) or "CÔNG SUẤT" in web_text:
            # Structure the Low Noon Peak row
            row_noon = [date_str, "Thấp điểm trưa"] + noon_values
            # Structure the High Evening Peak row
            row_evening = [date_str, "Cao điểm tối"] + evening_values
            
            # Add both structured rows to the final export array
            all_excel_rows.append(row_noon)
            all_excel_rows.append(row_evening)
            
            # FIXED HERE: Log to log.txt instead of terminal
            logging.info(f"-> Successfully processed: {date_str}")
        else:
            # FIXED HERE: Log to log.txt instead of terminal
            logging.warning(f"-> No data found or empty page for: {date_str}")

    except Exception as e:
        # FIXED HERE: Log the error details directly into log.txt
        logging.error(f"Skipping {date_str} due to error: {e}")
        # Crucial step: advance the loop date before continuing to prevent infinite loops on failure
        start_date += timedelta(days=1)
        continue

    # Advance to the next day if the current iteration runs successfully
    start_date += timedelta(days=1)

# 3. Compile the accumulated data matrix and export to Excel
if all_excel_rows:
    final_df = pd.DataFrame(all_excel_rows, columns=excel_columns)
    
    # Export directly to an Excel file with a flat structure (index=False removes pandas row numbers)
    output_filename = "z9_temp.xlsx"
    final_df.to_excel(output_filename, index=False)
    
    logging.info(f"[SUCCESS] All available data has been written perfectly to '{output_filename}'!")
    print(f"\n[SUCCESS] All available data has been written perfectly to '{output_filename}'!\n")
else:
    logging.error("[FAILED] No valid data collected to export.")
    print("\n[FAILED] No valid data collected to export.\n")