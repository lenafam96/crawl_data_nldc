import requests
import pandas as pd
from datetime import datetime, timedelta

# Define start and end dates
start_date = pd.to_datetime("01/12/2021", format="%d/%m/%Y")
end_date = pd.to_datetime("01/12/2021", format="%d/%m/%Y")

# Generate daily dates between start and end date (inclusive)
date_range = pd.date_range(start_date, end_date, freq="D")

# Initialize an empty DataFrame to store the results
all_days_df = []

# Iterate over the date range, Fetch data from the API
for date in date_range:
    date_str = date.strftime('%d/%m/%Y')
    url = f"https://www.nsmo.vn/Dashboard/GetSoLieuVanHanhNlttNgay?ngay={date_str}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data_raw = response.json()
        # Convert to DataFrame
        vanHanh = data_raw["result"]["data"]
    except Exception as e:
        print(f"Skipping {date_str} due to error: {e}")
        continue

    # Extract the required values from the API response
    # Map them directly into a dictionary with your requested column names
    data_for_day = {
        "Ngày": [date_str],
        "Solar (MW)": [vanHanh.get("solarMax", 0)],
        "Solar COD (MW)": [vanHanh.get("solarCOD", 0)],
        "Solar Energy (MWh)": [vanHanh.get("solarEnergy", 0)],
        "Wind (MW)": [vanHanh.get("windMax", 0)],
        "Wind COD (MW)": [vanHanh.get("windCOD", 0)],
        "Wind Energy (MWh)": [vanHanh.get("windEnergy", 0)],
        "Biomass (MW)": [vanHanh.get("biomassMax", 0)],
        "Biomass COD (MW)": [vanHanh.get("biomassCOD", 0)],
        "Biomass Energy (MWh)": [vanHanh.get("biomassEnergy", 0)],
        "Total (MW)": [vanHanh.get("totalMax", 0)],
        "Total COD (MW)": [vanHanh.get("totalCOD", 0)],
        "Total Energy (MWh)": [vanHanh.get("totalEnergy", 0)],
    }
    # Create a DataFrame for the current day (1 row with 5 columns)
    single_day_df = pd.DataFrame(data_for_day)
    # Save dataframe to final list
    all_days_df.append(single_day_df)

# Concatenate all daily dataframes into one final DataFrame
final_result_df = pd.concat(all_days_df, axis=0)
# Display the final DataFrame
# print(final_result_df)
# Export DataFrame to Excel
final_result_df.to_excel("Tong_hop_van_hanh_NLTT.xlsx", index=False)
print("Finished")