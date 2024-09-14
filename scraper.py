import requests
from bs4 import BeautifulSoup
import pandas as pd


def josaa_scrape(year, round, isCurrYear):
    """
    Sample usage: df = josaa_scrape("2024", "1", True)
    Sample usage: df = josaa_scrape("2023", "1", False)
    df.info()
    """
    old_year_url = 'https://josaa.admissions.nic.in/applicant/seatmatrix/openingclosingrankarchieve.aspx'
    curr_year_url = 'https://josaa.admissions.nic.in/applicant/SeatAllotmentResult/CurrentORCR.aspx'

    params = {
        "ctl00$ContentPlaceHolder1$ddlInstype": "ALL",
        "ctl00$ContentPlaceHolder1$ddlInstitute": "ALL",
        "ctl00$ContentPlaceHolder1$ddlBranch": "ALL",
        "ctl00$ContentPlaceHolder1$ddlSeatType": "ALL",
        "ctl00$ContentPlaceHolder1$btnSubmit": "Submit"
    }

    with requests.Session() as s:
        url = curr_year_url if isCurrYear else old_year_url
        R = s.get(url)
        data = {}

        if not isCurrYear:
            data.update({tag['name']: tag['value'] for tag in BeautifulSoup(R.content, 'lxml').select('input[name^=__]')})
            data["ctl00$ContentPlaceHolder1$ddlYear"] = year
            R = s.post(url, data=data)

        data.update({tag['name']: tag['value'] for tag in BeautifulSoup(R.content, 'lxml').select('input[name^=__]')})
        data["ctl00$ContentPlaceHolder1$ddlroundno"] = round
        R = s.post(url, data=data)

        for key, value in params.items():
            data.update({tag['name']: tag['value'] for tag in BeautifulSoup(R.content, 'lxml').select('input[name^=__]')})
            data[key] = value
            R = s.post(url, data=data)

    table = BeautifulSoup(R.text, 'lxml').find(id='ctl00_ContentPlaceHolder1_GridView1')
    df = pd.read_html(table.prettify())[0]
    df.dropna(inplace=True, how="all")

    df["Year"] = year
    df["Round"] = round
    # code commented because PwD rank contains P at end, e.g. 150P
    # df['Opening Rank'] = df['Opening Rank'].astype(int)
    # df['Closing Rank'] = df['Closing Rank'].astype(int)
    df['Opening Rank'] = df['Opening Rank']
    df['Closing Rank'] = df['Closing Rank']

    return df

def main():
    years = [
        # "2024",
        # "2023",
        # "2022",
        "2021",
        # "2018",
        # "2017",
        # "2016"
    ]

    rounds = [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        # "7"
    ]

    for year in years:
        for Round in rounds:
            print(Round, year)
            data = josaa_scrape(year, Round, False)
            print(data.shape)
            data.to_csv(path_or_buf=year + "-" + Round + ".csv", index=False)


if __name__ == "__main__":
    main()
