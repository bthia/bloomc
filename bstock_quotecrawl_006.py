# -*- coding: utf-8 -*-
"""
    This module read a list of stock ticker/symbol from bigquery and
    gets pull quote information from website
"""

import sys
import getopt
import time
import json
import re
import requests
from bs4 import BeautifulSoup as bs
from google.cloud import bigquery


#################################################################################
# Define module level constant
#################################################################################
ITEMPROPLIST = [r'name',
                r'tickerSymbol',
                r'exchange',
                r'price',
                r'priceChange',
                r'priceCurrency']

DATABOXREF = [r'dataBox.openprice.numeric',
              r'dataBox.previousclosingpriceonetradingdayago.numeric',
              r'dataBox.volume.numeric',
              r'dataBox.marketcap.numeric']

DATABOXRANGEREF = [r'dataBox.rangeoneday',
                   r'dataBox.range52weeks']

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

ITEMPROPLISTSTART = r'snapshotSummary'
ITEMPROPLISTSTARTPOS = 1
KEYSTATSSTART = r'"keyStatsList":[{'
KEYSTATSSTARTPOS = 1

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
def getdatabox(htmlsoup):
    """
        Look for the keyword Databox and extract its content
        """
    quotepagesnapshot = htmlsoup.select_one("section.quotePageSnapshot")
    subsection = quotepagesnapshot.select("section")
    
    for databoxitem in DATABOXREF:
        sssectionstr = "section."+databoxitem
        for subsetionitem in subsection:
            datasection = subsetionitem.select_one(sssectionstr)
            if datasection is not None:
                # print(datasection.select_one("span").text, datasection.select_one("div").text)
                m_stkinfo[datasection.select_one("span").text] = datasection.select_one("div").text
                break

    """
    Handle situation for ranges
    """
    for databoxitem in DATABOXRANGEREF:
        sssectionstr = "section."+databoxitem
        for subsetionitem in subsection:
            datasection = subsetionitem.select_one(sssectionstr)
            if datasection is not None:
                lowkeystr = datasection.select_one("span").text + "L"
                highkeystr = datasection.select_one("span").text + "H"
                m_stkinfo[lowkeystr] = datasection.select_one("span.textLeft").text
                m_stkinfo[highkeystr] = datasection.select_one("span.textRight").text
                break

#################################################################################
# Get Industry and Sector from Bloomberg
#################################################################################
def getindsec(htmlsoup):
    """
        Look for the keyword Databox and extract its content
        """
    scriptlist = htmlsoup.select("script")
    dataitem = [scriptitem for scriptitem in scriptlist if "bicsIndustry" in scriptitem.text][0]
    jstring = re.findall("({.+bicsIndustry.+});",dataitem.text)[0]
    jobj = json.loads(jstring)
    bicsIndustry = jobj["quote"]["bicsIndustry"]
    bicsSector = jobj["quote"]["bicsSector"]
    
    m_stkinfo["Sector"] = bicsSector
    m_stkinfo["Industry"] = bicsIndustry

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
# This program crawl bloomberg website for a particular stock
#################################################################################
def quote_crawl(stockcode, exchangecode):
    """
        Crawl program of a particular stock
        Go through bloomberg website to get data
        """
    exstkcode = ''
    urlstring = 'https://www.bloomberg.com/quote/'
    
    # Update current time and update stk and exchange code in bloomberg format
    currdate = time.strftime("%Y-%m-%d")
    exstkcode = stockcode.upper()+":"+exchangecode.upper()
    urlstring = urlstring + exstkcode
    m_stkinfo["quoteDate"] = currdate
    
    # Get htmltext from the website
    response = requests.get(urlstring)
    htmltext = response.text
    htmlsoup = bs(htmltext,"html.parser")
    
    # Process htmltext with htmltext that has reference itemProp
    getitemprop(htmltext)
    
    # Process htmltext with htmltext that has reference databox
    getdatabox(htmlsoup)
    
    # Process htmlsoup to get Industry and Secotr
    getindsec(htmlsoup)
    
    # Process htmltext with htmltext that has reference keystatistics
    getkeystats(htmltext)
    
    for itemprop in m_stkinfo.keys():
        print(itemprop + " = " + m_stkinfo[itemprop])

def bstock_tickerlistCrawl():
    client = bigquery.Client()
    query = """
        SELECT stkCode, exchange
        FROM `bloom_stock.tb_tickerlist`
        ORDER BY stkCode;
        """

    query_params = []
    job_config = bigquery.QueryJobConfig()
    job_config.query_parameters = query_params
    query_job = client.query(query, job_config=job_config)
                    
    query_job.result()  # Wait for job to complete
                    
    # Print the results.
    destination_table_ref = query_job.destination
    table = client.get_table(destination_table_ref)
    for row in client.list_rows(table):
        # print(row.stkCode, row.exchange)
        quote_crawl(row.stkCode, row.exchange)
        print()

def main():
# list_rows("bloom_stock","bstocklist")
# query_named_params("sonnets", 10)
    bstock_tickerlistCrawl()

if __name__ == "__main__":
    main()

