import requests
from bs4 import BeautifulSoup

#################################################################################
# Main Program
# ------------------------------
# Run 3 Functions to get 3 sets of strings
# 1. Max, Avg and Min RSI based on Indices
# 2. Stock details of shares that are with RSI > 70 (Overbought) or < 30 (Oversold)
# 3. Stock details of shares that have Tech Indicator Alert
#
#################################################################################
def main():
    #page = requests.get("https://sg.finance.yahoo.com/quote/0700.HK?p=0700.HK")
    #page = requests.get("https://www.google.com.sg/search?tbm=fin&q=HKG:+0700")
    # page = requests.get("http://money.cnn.com/quote/quote.html?symb=AAPL")

    page = requests.get("https://www.bloomberg.com/quote/700:HK")
    print(page.status_code)
    # print("\n\nContent\n\n")
    # print(page.content)

    soup = BeautifulSoup(page.content, 'html.parser')
    print("\n\nSoup Formatted\n\n")
    print(soup.prettify())

    #print("\n\nlist info\n\n")
    #print(list(soup.children))

if __name__ == '__main__':
    main()
