# -*- coding: utf-8 -*-
"""
    This module list table info needed for bloomberg stock analysis
"""

# Imports the Google Cloud client library
import sys
from google.cloud import bigquery

def list_rows(dataset_id, table_id, project=None):
    """Prints rows in the given table.
        
        Will print 25 rows at most for brevity as tables can contain large amounts
        of rows.
        
        If no project is specified, then the currently active project is used.
        """
    bigquery_client = bigquery.Client(project=project)
    dataset_ref = bigquery_client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)
    
    # Get the table from the API so that the schema is available.
    table = bigquery_client.get_table(table_ref)
    
    # Load at most 25 results.
    rows = bigquery_client.list_rows(table, max_results=2000)
    
    # Use format to create a simple table.
    format_string = '{!s:<16} ' * len(table.schema)
    
    # Print schema field names
    field_names = [field.name for field in table.schema]
    print(format_string.format(*field_names))
    
    for row in rows:
        print(format_string.format(*row))

def query_named_params(corpus, min_word_count):
    client = bigquery.Client()
    query = """
        SELECT word, word_count
        FROM `bigquery-public-data.samples.shakespeare`
        WHERE corpus = @corpus
        AND word_count >= @min_word_count
        ORDER BY word_count DESC;
        """
    query_params = [
                    bigquery.ScalarQueryParameter('corpus', 'STRING', corpus),
                    bigquery.ScalarQueryParameter(
                                                  'min_word_count', 'INT64', min_word_count)
                    ]
    job_config = bigquery.QueryJobConfig()
    job_config.query_parameters = query_params
    query_job = client.query(query, job_config=job_config)
                    
    query_job.result()  # Wait for job to complete
                    
    # Print the results.
    destination_table_ref = query_job.destination
    table = client.get_table(destination_table_ref)
    for row in client.list_rows(table):
        print(row)

def bstocksymbol_listinorder():
    client = bigquery.Client()
    query = """
        SELECT symbol, exchange
        FROM `bloom_stock.bstocklist`
        ORDER BY symbol;
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
        print(row.symbol, row.exchange)

def main(argv):
# list_rows("bloom_stock","bstocklist")
# query_named_params("sonnets", 10)
    bstocksymbol_listinorder()

if __name__ == "__main__":
    main(sys.argv[1:])

