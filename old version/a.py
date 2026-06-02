from config import session
from bs4 import BeautifulSoup
from get_thong_so_vh import thong_so_vh
from get_cong_suat_hd import cong_suat_hd
from datetime import datetime, timedelta

with open ("thong_so_vh.csv", "w", encoding='utf-8') as f:
    f.write('')

with open ("cong_suat_hd.csv", "w", encoding='utf-8') as f:
    f.write('')

start_date = datetime(2025, 1, 1)
while start_date < datetime(2025, 1, 2):
    day = start_date.date().strftime("%d")
    month = start_date.date().strftime("%m")
    year = start_date.date().strftime("%Y")

    cong_suat_hd_result = BeautifulSoup(cong_suat_hd(day, month, year, session))

    value = cong_suat_hd_result.find_all("td", class_="text-center")

    with open ("cong_suat_hd.csv", "a", encoding='utf-8') as f:
        f.write(f"{day}/{month}/{year}|")
        for i in range(0, len(value),2):
            f.write(f"{value[i].get_text().strip()}|{value[i+1].get_text().strip()}|")
        f.write("\n")


    if (start_date >= datetime(2025, 1, 2)):
        result = BeautifulSoup(thong_so_vh(day, month, year, session))

        # get content of div with class = "nameColum mb-3"
        nameColum = result.find_all("div", class_="row px-5 py-3 fw-bold fs-6 text-gray-800")
        group = result.find_all("div", class_="col px-5")
        don_vi = result.find_all("div", class_="col px-5 text-left")
        with open ("thong_so_vh.csv", "a", encoding='utf-8') as f:
            cong_suat_max = nameColum[0].get_text().split(":")[1].strip().split(" (Lúc ")[0].strip()
            _time = nameColum[0].get_text().split(" (Lúc ")[-1].replace(")", "").strip()
            san_luong = nameColum[1].get_text().split(":")[1].strip()
            f.write(f"{day}/{month}/{year}|{_time}|{cong_suat_max}|{san_luong}|")
            for i in range(0, len(don_vi)):
                f.write(f"{group[i*2+1].get_text().strip()}|{don_vi[i].get_text().strip()}|")
            f.write("\n")
        
    print(f"Done {day}/{month}/{year}")
    
    start_date += timedelta(days=1)