#!/usr/bin/env python
# coding: utf-8

import os
import argparse

from time import time

import pandas as pd
from sqlalchemy import create_engine
import pyarrow.parquet as pq


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    # the backup files are gzipped, and it's important to keep the correct extension
    # for pandas to be able to open the file
    file_name = "output.parquet"
    os.system(f"curl -o {file_name} {url}")

    df = pd.read_parquet(file_name)

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    # Open Parquet file
    parquet_file = pq.ParquetFile(file_name)

    # Read in chunks
    for batch in parquet_file.iter_batches(batch_size=100000):
        df_chunk = batch.to_pandas()
        # Process your chunk here

        df_chunk.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df_chunk.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

        df_chunk.to_sql(name=table_name, con=engine, if_exists='append')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest parquet data to Postgres')

    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--table_name', required=True, help='name of the table where we will write the results to')
    parser.add_argument('--url', required=True, help='url of the csv file')

    args = parser.parse_args()

    main(args)
