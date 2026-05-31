import requests
import pandas as pd
from datetime import datetime, timedelta

# Define start and end dates
start_date = pd.to_datetime("30/05/2026", format="%d/%m/%Y")
end_date = pd.to_datetime("30/05/2026", format="%d/%m/%Y")

# Generate daily dates between start and end date (inclusive)
date_range = pd.date_range(start_date, end_date, freq="D")

# Initialize an empty DataFrame to store the results
all_days_df = []

for date in date_range:
    url = f"https://www.nsmo.vn/Dashboard/GetBcsxChartDataPhanBoTheoLoaiHinh?ngay={date.strftime('%d/%m/%Y')}"
    response = requests.get(url)
    data_raw = response.json()
    categories_data = data_raw["result"]

    # Extract categories and their corresponding power values
    categories = [item['category'] for item in categories_data]
    values = [item['value'] for item in categories_data]
    data_for_day = {
        date.strftime('%d/%m/%Y'): categories,
        "Công suất": values
    }


print(categories_data)