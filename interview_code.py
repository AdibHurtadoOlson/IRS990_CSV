import requests
import re
from bs4 import BeautifulSoup


# Gets the '.zip' urls from the IRS990 webpage using the '2021' link
def get_urls():
    months = []
    month_urls = []
    month_names = []

    with open("irs990.xml", 'r') as file:
        data = file.read()

    # Reads the url in the irs990.xml and creates an irs_soup BS4
    xml_bs_data = BeautifulSoup(data, "xml").find("ListBucketResult")
    irs_bs_request = requests.get(xml_bs_data["xmlns"])
    irs_soup = BeautifulSoup(irs_bs_request.content, "html.parser")

    # Parses webpage, finding all the '.csv' urls on the webpage
    for month in irs_soup.findAll("p"):
        if month.find("strong") is not None and month.find("a") is not None:
            month_urls.append(month.find("a")["href"])
            month_names.append(("".join(re.split("[^a-zA-Z]*", month.text))).split("I")[0])

    # Adds all links to list
    months.append(month_names)
    months.append(month_urls)

    return months


# Download all '.csv' files from list
def download_files():
    months = get_urls()

    month_files = []

    # For every month, create csv file using month name
    for month_counter in range(len(months[0])):
        month_file = "data/" + months[0][month_counter] + ".csv"
        req = requests.get(months[1][month_counter])

        # Since files are larger, writes bits to 'month' file in chunks
        with open(month_file, "wb") as file:
            for chunk in req.iter_content(chunk_size=65536):
                file.write(chunk)

        month_files.append(month_file)

    return month_files


def read_data():
    month_files = download_files()
