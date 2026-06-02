def thong_so_vh(day,month,year,session):
    url = f"https://www.nsmo.vn/HTDThongSoVH?day={day}%2F{month}%2F{year}"
    
    payload = {}

    response = session.get(url, data=payload)

    return response.text
