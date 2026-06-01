import requests
import pandas as pd
from datetime import datetime

# 1. Define date range for the API URL
start_date = "01/01/2021"
end_date = "31/05/2026"

url = f"https://www.nsmo.vn/Dashboard/GetSoLieuCongSuatMtmn?tungay={start_date}&denngay={end_date}"

try:
    response = requests.get(url)
    response.raise_for_status()
    data_raw = response.json()
    corporations_data = data_raw["result"]["data"]
except Exception as e:
    print(f"Error fetching data from API: {e}")
    corporations_data = []

# Order of corporate rows requested
requested_rows = ["EVNNPC", "EVNHANOI", "EVNCPC", "EVNSPC", "EVNHCMC"]

# 2. Parse raw data into a structured flat list
parsed_records = []
for corp in corporations_data:
    corp_name = corp["name"]
    for item in corp["data"]:
        # Parse timestamp (e.g., "2025-01-01T06:30:00")
        dt_obj = datetime.strptime(item["time"], "%Y-%m-%dT%H:%M:%S")
        date_label = dt_obj.strftime("%d/%m/%Y")
        time_label = dt_obj.strftime("%H:%M")
        
        # Filter: Only keep time slots between 06:00 and 19:00 inclusive
        if "06:00" <= time_label <= "19:00":
            parsed_records.append({
                "Date": date_label,
                "Corporation": corp_name,
                "time": time_label,
                "value": item["value"]
            })

# Convert parsed records into a temporary helper DataFrame
flat_df = pd.DataFrame(parsed_records)
# 3. Process and reconstruct the DataFrame day by day
all_days_df = []

if not flat_df.empty:
    for date_group, group_df in flat_df.groupby("Date", sort=False):
        
        # Pivot by 'Corporation', temporarily keeping 'Date' out of index to avoid automatic cell merging
        pivoted_df = group_df.pivot(index="Corporation", columns="time", values="value")
        
        # Reindex rows to match the exact requested corporate order
        pivoted_df = pivoted_df.reindex(requested_rows)
        
        # Insert the "Date" column at the first position of the current daily DataFrame
        pivoted_df.insert(0, "Date", date_group)
        
        # Reset index to turn "Corporation" from an index into a regular data column
        pivoted_df = pivoted_df.reset_index()
        
        all_days_df.append(pivoted_df)

# 4. Combine all daily blocks and export
if all_days_df:
    final_result_df = pd.concat(all_days_df, axis=0)
    # Rearrange column order to ensure "Date" comes before "Corporation"
    cols = ["Date", "Corporation"] + [c for c in final_result_df.columns if c not in ["Date", "Corporation"]]
    final_result_df = final_result_df[cols]
    # Export directly to Excel (Overwriting existing file)
    output_filename = "Cong_suat_MTMN.xlsx"
    final_result_df.to_excel(output_filename, index=False)
    print(f"\nData successfully exported and overwrote: '{output_filename}'")
else:
    print("No valid data available to process.")