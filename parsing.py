import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime


def get_cmc_data():
    url = "https://coinmarketcap.com/top/mcap/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table', {'class': 'cmc-table'})
    rows = table.find_all('tr')

    data = []
    for row in rows[1:]:  
        cols = row.find_all('td')
        name = cols[2].text.strip()
        mc = float(cols[3].text.replace(',', '').strip())
        mp = round((mc / sum([float(row.find('td').text.replace(',', '').strip()) for row in rows[1:]]) * 100), 2)

        data.append({'Name': name, 'MC': mc, 'MP': mp})

    return data


def write_cmc_top(data):
    now = datetime.now().strftime("%H.%M %d.%m.%Y")
    filename = f"{now}.csv"

    df = pd.DataFrame(data)
    df.to_csv(filename, sep=' ', index=False)


if __name__ == "__main__":
    data = get_cmc_data()
    write_cmc_top(data)