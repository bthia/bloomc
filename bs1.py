import requests

#page = requests.get("https://sg.finance.yahoo.com/quote/0700.HK?p=0700.HK")
#page = requests.get("https://www.google.com.sg/search?tbm=fin&q=HKG:+0700")
# page = requests.get("http://money.cnn.com/quote/quote.html?symb=AAPL")

page = requests.get("https://www.bloomberg.com/quote/700:HK")
print(page.status_code)
# print("\n\nContent\n\n")
# print(page.content)

from bs4 import BeautifulSoup
soup = BeautifulSoup(page.content, 'html.parser')
print("\n\nSoup Formatted\n\n")
print(soup.prettify())

#print("\n\nlist info\n\n")
#print(list(soup.children))
