# -*- coding: utf-8 -*-
"""
    This module create tables needed for bloomberg stock analysis
"""

# Imports the Google Cloud client library
import sys
from google.cloud import bigquery

def create_table(dataset_id, table_id, project=None):
    """
        Creates a simple table in the given dataset.
        
        If no project is specified, then the currently active project is used.
    """
    bigquery_client = bigquery.Client(project=project)
    dataset_ref = bigquery_client.dataset(dataset_id)
    
    table_ref = dataset_ref.table(table_id)
    table = bigquery.Table(table_ref)
    
    # Set the table schema
    table.schema = (
                    bigquery.SchemaField('StockCode', 'STRING'),
                    bigquery.SchemaField('Exchange', 'INTEGER'),
                    )
        
    table = bigquery_client.create_table(table)
                    
    print('Created table {} in dataset {}.'.format(table_id, dataset_id))

def main(argv):
    create_table("bloom_stock","bstocklist")

if __name__ == "__main__":
    main(sys.argv[1:])

