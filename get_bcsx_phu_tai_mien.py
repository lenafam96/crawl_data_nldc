import requests
import pandas as pd
from datetime import datetime, timedelta

# Define start and end dates
start_date = pd.to_datetime("01/01/2025", format="%d/%m/%Y")
end_date = pd.to_datetime("31/12/2025", format="%d/%m/%Y")

# Generate daily dates between start and end date (inclusive)
date_range = pd.date_range(start_date, end_date, freq="D")

# Initialize an empty DataFrame to store the results
all_days_df = []

# Iterate over the date range, Fetch data from the API
for date in date_range:
    url = f"https://www.nsmo.vn/Dashboard/GetBcsxChartDataPhuTai?ngay={date.strftime('%d/%m/%Y')}"
    response = requests.get(url)
    data_raw = response.json()
    # Convert to DataFrame
    phuTai = data_raw["result"]
    # Extract the 'hour' values for the 'Thời gian' row
    time_hours = [item['hour'] for item in phuTai[0]['data']]
    # Prepare data for the DataFrame, with 'Thời gian' as the first 'row' (which will become the first column after transpose)
    data_for_df = {date.strftime('%d/%m/%Y'): time_hours}
    # Add data for each region
    for region_data in phuTai:
        region_name = region_data['name']
        values = [item['value'] for item in region_data['data']]
        data_for_df[region_name] = values
    # Create a temporary DataFrame. At this point, 'Thời gian' and region names are columns.
    temp_df = pd.DataFrame(data_for_df)
    # Transpose the DataFrame to have 'Thời gian' and regions as index (rows)
    single_day_df = temp_df.T
    # Rename the index to match the user's request
    single_day_df = single_day_df.rename(index={'Bắc': 'Miền Bắc', 'Trung': 'Miền Trung', 'Nam': 'Miền Nam'})
    # Rename columns from 0-47 to 1-48
    single_day_df.columns = range(1, 49)
    # Save dataframe to final list
    all_days_df.append(single_day_df)

# Concatenate all daily dataframes into one final DataFrame
final_result_df = pd.concat(all_days_df, axis=0)
# Display the final DataFrame
# print(final_result_df)
# Export DataFrame to Excel
final_result_df.to_excel("Phu_tai_VM_2025.xlsx")
print("Finished")