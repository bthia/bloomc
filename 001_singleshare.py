# -*- coding: utf-8 -*-
"""Example Google style docstrings.
    This module gets data for a single share on Bloomberg.
    $ python 001_singleshare.py -e <exchangecode> -s <stock ticket symbol>
    Section breaks are created by resuming unindented text. Section breaks
    are also implicitly created anytime a new section starts.
    .. _Google Python Style Guide:
    http://google.github.io/styleguide/pyguide.html
"""

import sys
import getopt
import time
import re
import requests

#################################################################################
# Define module level constant
#################################################################################
ITEMPROPLIST = [r'name',
                r'tickerSymbol',
                r'exchange',
                r'price',
                r'priceChange',
                r'priceCurrency']

ITEMPROPLISTSTART = r'snapshotSummary'

KEYSTATS = [r'priceEarningsRatio',
            r'estimatedPriceEarningsRatioCurrentYear',
            r'estimatedPriceEarningsToGrowthRatio',
            r'sharesOutstanding',
            r'priceToBookRatio',
            r'priceToSalesRatio',
            r'totalReturn1Year',
            r'averageVolume30Day',
            r'earningsPerShare',
            r'estimatedEarningsPerShareCurrentYear',
            r'dividend',
            r'lastDividendReported']

#################################################################################
# Define module level variable
#################################################################################
m_stkinfo = {}

def main(argv):
    """
        main program
        Go through bloomberg website to get data
    """
    exchangecode = ''
    stockcode = ''
    exstkcode = ''
    urlstring = 'https://www.bloomberg.com/quote/'

    try:
        opts, args = getopt.getopt(argv, "he:s:", ["exchangecode=", "stockcode="])
    except getopt.GetoptError:
        print('0001_singleshare.py -e <exchangecode> -s <stockcode>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('001_singleshare.py -e <exchangecode> -s <stockcode>')
            sys.exit()
        elif opt in ("-e", "--exchangecode"):
            exchangecode = arg
        elif opt in ("-s", "--stockcode"):
            stockcode = arg

    if (exchangecode == '' or stockcode == ''):
        print('0001_singleshare.py -e <exchangecode> -s <stockcode>')
        sys.exit()

    # Update current time and update stk and exchange code in bloomberg format
    currdate = time.strftime("%Y-%m-%d")
    exstkcode = stockcode.upper()+":"+exchangecode.upper()
    urlstring = urlstring + exstkcode

    response = requests.get(urlstring)
    htmltext = response.text

    # Split to get itemProp data more easily
    # *** not ideal but not able to find other choice easily
    splitList1 = htmltext.split(ITEMPROPLISTSTART)
    # print(splitList1[1])

    for itemprop in ITEMPROPLIST:
        matchstr = "(.*)<meta itemProp=\""+itemprop+"\" content=\"(?P<mvar>(.*?))\"/>"
        matchobj = re.match(matchstr, splitList1[1])
        if matchobj:
            m_stkinfo[itemprop] = matchobj.group("mvar")

    for itemprop in ITEMPROPLIST:
        print(itemprop + " = " + m_stkinfo[itemprop])


if __name__ == "__main__":
    main(sys.argv[1:])
