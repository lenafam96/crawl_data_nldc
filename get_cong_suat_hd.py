def cong_suat_hd(day,month,year,session):
    url = f"https://www.nldc.evn.vn/HTDCongSuatHD?day={day}%2F{month}%2F{year}"

    payload = {}

    response = session.get(url, data=payload)

    return response.text
