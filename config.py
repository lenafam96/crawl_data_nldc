import requests

session = requests.session()
session.cookies.clear()
session.headers.update({
    'Accept': 'text/plain, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8,vi;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type': 'application/text; charset=utf-8',
    'Cookie': '.AspNetCore.Antiforgery.ovZy99TDzzU=CfDJ8M7BBblHs0ZEv_a3o9khR4r4nCaqyweYf8lS62uTxtjGUXyLZBpWmk7sKPvuqzV_IA1pdkoFweriuv100VRKwt9236sqDCdccWXsVv6FDTSq4fLe9fyhOXO7UMGrjbg2RaNxiSNKbDLet4TdDlt0IZQ; Abp.TenantId=1; .AspNetCore.Culture=c%3Dvi%7Cuic%3Dvi; XSRF-TOKEN=CfDJ8M7BBblHs0ZEv_a3o9khR4py8y2TMIa8ULt09UF8iiOAJDYdp-4bLSpeMDW3t2k2CY83QkOs3hld5eD7AnuHQe494YPrj796j2HPQQVX-qgr94z61LCwTvPqx7u4uBhdS4lSdOz5CI1iuL4FcHWjv50',
    'Referer': 'https://www.nsmo.vn/dashboard/tonghop',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'X-XSRF-TOKEN': 'CfDJ8M7BBblHs0ZEv_a3o9khR4py8y2TMIa8ULt09UF8iiOAJDYdp-4bLSpeMDW3t2k2CY83QkOs3hld5eD7AnuHQe494YPrj796j2HPQQVX-qgr94z61LCwTvPqx7u4uBhdS4lSdOz5CI1iuL4FcHWjv50',
    'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"'
})