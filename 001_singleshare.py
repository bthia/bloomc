#!/usr/bin/python

import sys, getopt
import requests
from bs4 import BeautifulSoup

#################################################################################
# Main Program
# ------------------------------
# Get shareprice of a single share and print on screen
#
#################################################################################
def main(argv):
    
    exchangecode = ''
    stockcode = ''
    exstkcode = ''
    urlstring = 'https://www.bloomberg.com/quote/'
    
    try:
        opts, args = getopt.getopt(argv, "he:s:", ["exchangecode=","stockcode="])
    except getopt.GetoptError:
        print('0001_singleshare.py -e <exchangecode> -s <stockcode>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('001_singleshare.py -e <exchangecode> -s <stockcode>')
            sys.exit()
        elif opt in ("-e","--exchangecode"):
            exchangecode = arg
        elif opt in ("-s", "--stockcode"):
            stockcode = arg

    exstkcode = stockcode.upper()+":"+exchangecode.upper()   # change to the format for bloomber uppercase
    urlstring = urlstring + exstkcode

# Debug code
#print("Exchange is ", exchangecode)
#print("Stock is", stockcode)
#print("Search string is", exstkcode)
#print("URL string is ", urlstring)
#sys.exit()

    page = requests.get(urlstring)
    print(page.status_code)
    # print("\n\nContent\n\n")
    # print(page.content)

    soup = BeautifulSoup(page.content, 'html.parser')
    print("\n\nSoup Formatted\n\n")
    print(soup.prettify())

    #print("\n\nlist info\n\n")
    #print(list(soup.children))

if __name__ == "__main__":
    main(sys.argv[1:])
