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
ITEMPROPLISTSTARTPOS = 1
KEYSTATSSTART = r'"keyStatsList":[{'
KEYSTATSSTARTPOS = 1

KEYSTATSLIST = [r'peRatio',
                r'bloombergPeRatio',
                r'bloombergPegRatio',
                r'sharesOutstanding',
                r'priceToBookRatio',
                r'priceToSalesRatio',
                r'oneYearReturn',
                r'30DayVolume',
                r'eps',
                r'bloombergEpsCurrentYear',
                r'dividend',
                r'lastDividendReported']

#################################################################################
# Define module level variable
#################################################################################
m_stkinfo = {}

#################################################################################
# Get string between 2 substring
#################################################################################
def str_between(mystr, sstr, estr):
    # Find and validate before-part.
    pos_a = mystr.find(sstr)
    if pos_a == -1: return ""
    # Find and validate after part.
    pos_b = mystr.rfind(estr)
    if pos_b == -1: return ""
    # Return middle part.
    adjusted_pos_a = pos_a + len(sstr)
    if adjusted_pos_a >= pos_b: return ""
    return mystr[adjusted_pos_a:pos_b]

#################################################################################
# Get string before an item
#################################################################################
def str_before(mystr, sstr):
    # Find first part and return slice before it.
    pos_a = mystr.find(sstr)
    if pos_a == -1: return ""
    return mystr[0:pos_a]

#################################################################################
# Get data from bloomberg itemprop
#################################################################################
def getitemprop(htmltext):
    """
        Look for keyword itemProp in source
        Split to get itemProp data more easily
        *** not ideal but not able to find other choice easily
    """
    splitList = htmltext.split(ITEMPROPLISTSTART)

    # Handle situation when wrong symbol is keyed in
    # Prevent a wrong symbol disrupt execution when not able to split correctly
    if (len(splitList) <= ITEMPROPLISTSTARTPOS):
        return
    # print(splitList[1])

    for itemprop in ITEMPROPLIST:
        matchstr = "(.*)<meta itemProp=\""+itemprop+"\" content=\"(?P<mvar>(.*?))\"/>"
        matchobj = re.match(matchstr, splitList[ITEMPROPLISTSTARTPOS])
        if matchobj:
            m_stkinfo[itemprop] = matchobj.group("mvar")

#################################################################################
# Get Databox item from Bloomberg
#################################################################################
def getdatabox(htmltext):
    """
        Look for the keyword Databox and extract its content
    """

#################################################################################
# Get key statistics from Bloomberg
#################################################################################
def getkeystats(htmltext):
    """
        Look for the keyword keyStatsList and extract its content
    """
    strarray = [] # string array
    dicarray = [] # dictionary array
    
    splitList1 = htmltext.split(KEYSTATSSTART)
    # Handle situation when wrong symbol is keyed in
    # Prevent a wrong symbol disrupt execution when not able to split correctly
    if (len(splitList1) <= ITEMPROPLISTSTARTPOS):
        return
    
    splitList2 = splitList1[KEYSTATSSTARTPOS].split('}]')

    splitList = splitList2[0].split('},{')

    for strdic in splitList:
        mystr = strdic.replace("\"","")
        mystr = mystr.replace("bloomberg","est")
        mystr = mystr.replace("$snapshotDetails", "$keyStatistics")
        mykey = str_between(mystr, "$keyStatistics.", ",id")
        myvalue = str_between(mystr,"fieldValue:", ",translationId")
        m_stkinfo[mykey] = myvalue

#################################################################################
# Main program starts
#################################################################################
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

    # Get htmltext from the website
    response = requests.get(urlstring)
    htmltext = response.text

    # Process htmltext with htmltext that has reference itemProp
    getitemprop(htmltext)

    # Process htmltext with htmltext that has reference keystatistics
    getkeystats(htmltext)

    for itemprop in m_stkinfo.keys():
        print(itemprop + " = " + m_stkinfo[itemprop])


if __name__ == "__main__":
    main(sys.argv[1:])
