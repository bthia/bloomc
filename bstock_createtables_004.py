# -*- coding: utf-8 -*-
"""
    This module gets creates tables for stock analytics
    with data crawled from bloomberg
"""

import sys
from google.cloud import bigquery

def tickertable_create(dataset_id, project=None):
    """
        Create list of tickers
        To be used for crawling data
    """
    bigquery_client = bigquery.Client(project=project)
    dataset_ref = bigquery_client.dataset(dataset_id)
    
    table_id = 'tb_tickerlist'
    table_ref = dataset_ref.table(table_id)
    table = bigquery.Table(table_ref)
    
    # Set the table schema
    table.schema = (
                    bigquery.SchemaField('stkCode', 'STRING', mode='required'),
                    bigquery.SchemaField('exchange', 'STRING', mode='required'),
                    )
        
    table = bigquery_client.create_table(table)
                    
    print('Created table {} in dataset {}.'.format(table_id, dataset_id))

def stockpricetable_create(dataset_id, project=None):
    """
        Create list of daily stockprice
    """
    bigquery_client = bigquery.Client(project=project)
    dataset_ref = bigquery_client.dataset(dataset_id)
    
    table_id = 'dailyquote'
    table_ref = dataset_ref.table('tb_dayquote')
    table = bigquery.Table(table_ref)

    # Set the table schema
    table.schema = (
                    bigquery.SchemaField('quoteDate', 'DATE', mode='required'),
                    bigquery.SchemaField('stkCode', 'STRING', mode='required'),
                    bigquery.SchemaField('exchange', 'STRING'),
                    bigquery.SchemaField('sector', 'STRING'),
                    bigquery.SchemaField('industry', 'STRING'),
                    bigquery.SchemaField('price', 'FLOAT'),
                    bigquery.SchemaField('prevClose', 'FLOAT'),
                    bigquery.SchemaField('open', 'FLOAT'),
                    bigquery.SchemaField('LowDay', 'FLOAT'),
                    bigquery.SchemaField('highDay', 'FLOAT'),
                    bigquery.SchemaField('Low52w', 'FLOAT'),
                    bigquery.SchemaField('High52w', 'FLOAT'),
                    bigquery.SchemaField('vol', 'FLOAT'),
                    bigquery.SchemaField('vol30day', 'FLOAT'),
                    bigquery.SchemaField('mktCap', 'FLOAT'),
                    bigquery.SchemaField('pe', 'FLOAT'),
                    bigquery.SchemaField('dividend', 'FLOAT'),
                    bigquery.SchemaField('lastdividend', 'FLOAT'),
                    bigquery.SchemaField('estPe', 'FLOAT'),
                    bigquery.SchemaField('estPeg', 'FLOAT'),
                    bigquery.SchemaField('price2book', 'FLOAT'),
                    bigquery.SchemaField('price2sales', 'FLOAT'),
                    bigquery.SchemaField('sharesOutstanding', 'FLOAT'),
                    bigquery.SchemaField('oneYearReturn', 'FLOAT'),
                    bigquery.SchemaField('eps', 'FLOAT'),
                    bigquery.SchemaField('rsi10', 'FLOAT'),
                    bigquery.SchemaField('rsi14', 'FLOAT'),
                    bigquery.SchemaField('rsi20', 'FLOAT'),
                    bigquery.SchemaField('ema05', 'FLOAT'),
                    bigquery.SchemaField('ema12', 'FLOAT'),
                    bigquery.SchemaField('ema26', 'FLOAT'),
                    bigquery.SchemaField('ema50', 'FLOAT'),
                    bigquery.SchemaField('macd', 'FLOAT'),
                    bigquery.SchemaField('macd_ema9', 'FLOAT'),
                    bigquery.SchemaField('so', 'FLOAT'),
                    bigquery.SchemaField('so_ema3', 'FLOAT'),
                    )

    table = bigquery_client.create_table(table)
    print('Created table {} in dataset {}.'.format(table_id, dataset_id))
                                                                


#################################################################################
# Main program starts
#################################################################################
def main(argv):
    """
        main program
        create tables for profram
    """
    tickertable_create("bloom_stock")
    stockpricetable_create("bloom_stock")

if __name__ == "__main__":
    main(sys.argv[1:])
