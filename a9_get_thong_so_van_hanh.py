import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
import logging

# ==============================================================================
# USER CONFIGURATION
# ==============================================================================
start_date_str = "01/01/2025"
end_date_str = "31/05/2026"

# Excel output file name
output_filename = "z9_Thong_so_van_hanh.xlsx"


# ==============================================================================
# LOGGING CONFIGURATION (Ghi lịch sử chạy vào file log_thong_so_vh.txt)
# ==============================================================================
logging.basicConfig(
    filename='z9_Thong_so_van_hanh_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d/%m/%Y %H:%M:%S',
    encoding='utf-8'
)

# ==============================================================================
# INTEGRATED FUNCTION
# ==============================================================================
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

# Convert input strings to native datetime objects safely
start_date = datetime.strptime(start_date_str, "%d/%m/%Y")
end_date = datetime.strptime(end_date_str, "%d/%m/%Y")

# Fixed categories for the energy mix generation components
raw_categories = [
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
categories = [f"{cat} (tr. kWh)" for cat in raw_categories]
# Định nghĩa các tiêu đề cột theo cấu trúc phẳng 1 ngày = 1 dòng
excel_columns = [
    "Ngày",
    "Thời gian",
    "Pmax_TP (MW)", 
    "Pmax_đầu cực (MW)", 
    "SL_TP (tr. kWh)",
    "SL_đầu cực (tr. kWh)"
] + categories

# Array to store all structured rows across the entire date range
all_excel_rows = []

logging.info("Starting to crawl operational parameters data...")

# 2. Loop through each day in the date range
while start_date <= end_date:
    day = start_date.strftime("%d")
    month = start_date.strftime("%m")
    year = start_date.strftime("%Y")
    date_str = f"{day}/{month}/{year}"

    try:
        # Fetch the raw HTML source code
        html_raw = thong_so_vh(day, month, year)
        soup = BeautifulSoup(html_raw, "html.parser")
        web_text = soup.get_text()

        if "THÔNG SỐ VẬN HÀNH" in web_text or "Công suất lớn nhất" in web_text:
            
            # --- PHASE 1: Extract "Ước tính thương phẩm" block ---
            pmax_comm, time_comm, gen_comm = 0.0, "", 0.0
            comm_match = re.search(r"Tính với số liệu ĐMT mái nhà \(ước tính thương phẩm\):.*?Công suất lớn nhất trong ngày:\s*([\d.,]+)\s*MW\s*\(Lúc\s*([\d:]+)\).*?Sản lượng điện sản xuất và nhập khẩu:\s*([\d.,]+)\s*triệu kWh", web_text, re.DOTALL)
            if comm_match:
                pmax_comm = float(comm_match.group(1).replace(",", "."))
                time_comm = comm_match.group(2).strip()
                gen_comm = float(comm_match.group(3).replace(",", "."))

            # --- PHASE 2: Extract "Ước tính đầu cực" block ---
            pmax_term, time_term, gen_term = 0.0, "", 0.0
            term_match = re.search(r"Tính với số liệu ĐMT mái nhà \(ước tính đầu cực\):.*?Công suất lớn nhất trong ngày:\s*([\d.,]+)\s*MW\s*\(Lúc\s*([\d:]+)\).*?Sản lượng điện sản xuất và nhập khẩu:\s*([\d.,]+)\s*triệu kWh", web_text, re.DOTALL)
            if term_match:
                pmax_term = float(term_match.group(1).replace(",", "."))
                time_term = term_match.group(2).strip()
                gen_term = float(term_match.group(3).replace(",", "."))

            # --- PHASE 3: Extract generation mix components ---
            mix_values = []
            for i, cat in enumerate(raw_categories):
                next_cat = raw_categories[i+1] if i + 1 < len(raw_categories) else "$"
                pattern = re.escape(cat) + r"\s*([\d.,]+)\s*(?:triệu kWh|(?=" + re.escape(next_cat) + r"|$))"
                match = re.search(pattern, web_text, re.DOTALL)
                
                if match:
                    mix_values.append(float(match.group(1).replace(",", ".")))
                else:
                    mix_values.append(0.0)

            # --- PHASE 4: Combine everything into exactly ONE row
            single_day_row = [
                date_str,
                time_comm,
                pmax_comm, 
                pmax_term,
                gen_comm,
                gen_term,
            ] + mix_values

            # Append the single row to the master list
            all_excel_rows.append(single_day_row)
            
            logging.info(f"-> Successfully processed operational parameters: {date_str}")
        else:
            logging.warning(f"-> No operational data found or empty page for: {date_str}")

    except Exception as e:
        logging.error(f"Skipping operational data for {date_str} due to error: {e}")
        start_date += timedelta(days=1)
        continue

    # Advance to the next day
    start_date += timedelta(days=1)

# 3. Compile the accumulated data matrix and export to Excel
if all_excel_rows:
    final_df = pd.DataFrame(all_excel_rows, columns=excel_columns)
    
    # Save directly to an Excel file using the variable defined at the top
    final_df.to_excel(output_filename, index=False)
    
    logging.info(f"[SUCCESS] All data has been written perfectly to '{output_filename}'!")
    print(f"\n[SUCCESS] All available data has been written perfectly to '{output_filename}'!\n")
else:
    logging.error("[FAILED] No operational data collected to export.")
    print("\n[FAILED] No valid data collected to export.\n")