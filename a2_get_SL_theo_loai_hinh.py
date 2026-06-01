import requests
import pandas as pd
from datetime import datetime, timedelta

# Define start and end dates
start_date = pd.to_datetime("01/01/2021", format="%d/%m/%Y")
end_date = pd.to_datetime("31/05/2026", format="%d/%m/%Y")

# Generate daily dates between start and end date (inclusive)
date_range = pd.date_range(start_date, end_date, freq="D")

# Initialize an empty list to store the results
all_days_df = []

# Iterate over the date range, Fetch data from the API
for date in date_range:
    date_str = date.strftime('%d/%m/%Y')
    url = f"https://www.nsmo.vn/Dashboard/GetBcsxChartDataPhanBoTheoLoaiHinh?ngay={date_str}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data_raw = response.json()
        categories_data = data_raw["result"]
    except Exception as e:
        print(f"Skipping {date_str} due to error: {e}")
        continue

    # Extract categories and their corresponding power values
    categories = [item['category'] for item in categories_data]
    values = [item['value'] for item in categories_data]

    # Create a temporary DataFrame
    single_day_df = pd.DataFrame([values], columns=categories, index=[date_str])
    # Append the formatted daily DataFrame to the main tracking list
    all_days_df.append(single_day_df)

# Concatenate all daily dataframes into one final DataFrame
final_result_df = pd.concat(all_days_df, axis=0)

final_result_df.to_excel("Phan_bo_san_luong.xlsx")
print("Finished")