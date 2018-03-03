# -*- coding: utf-8 -*-
"""
    This module gets creates tables for stock analytics
    with data crawled from bloomberg
"""

import sys
from google.cloud import bigquery

def load_data_from_gcs(dataset_id, table_id, source):
    bigquery_client = bigquery.Client()
    dataset_ref = bigquery_client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)
    
    job = bigquery_client.load_table_from_uri(source, table_ref)
    
    job.result()  # Waits for job to complete
    
    print('Loaded {} rows into {}:{}.'.format(
                                              job.output_rows, dataset_id, table_id))


#################################################################################
# Main program starts
#################################################################################
def main(argv):
    """
        main program
        create tables for profram
    """
    load_data_from_gcs("bloom_stock","tb_tickerlist","gs://avatardata/hk.csv")

if __name__ == "__main__":
    main(sys.argv[1:])
