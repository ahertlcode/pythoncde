"""
Data Extractor

This script extracts data present in an html table on a webpage
with the url of the page know and a queryselect of the table know
either the class name or the id of the table.
"""
import urllib
from bs4 import BeautifulSoup
import pandas as pd

# pylint: disable=C0103

url = 'http://en.wikipedia.org/wiki/List_of_Presidents_of_the_United_States'
request = urllib.request.Request(url)
opener = urllib.request.build_opener()
response = opener.open(request)
soup = BeautifulSoup(response, "lxml")
table = soup.select_one("table.wikitable")

pres = []

body = [[td.text for td in row.find_all("td")] for row in table.select("tr + tr")]
for pos in range(0, len(body)):
    if len(body[pos]) > 3 and pos <= 80:
        _pstart = (body[pos][1].replace("\n", " ").split("(")[0]).split(" – ")[0]
        _pend = (body[pos][1].replace("\n", " ").split("(")[0]).split(" – ")[1]
        pres.append({
            "President" : str(" ".join(body[pos][3].replace("\n", " ").split(" ")[:3])),
            "Start" : str(_pstart),
            "End" : str(_pend),
            "Party" : str(body[pos][6].replace("\n", ""))})
dataset = pd.DataFrame(pres)
dataset.to_excel("presidents.xlsx")
