import boto3
import logging
import pandas as pd
from fastavro import writer, reader, parse_schema
from sqlalchemy import create_engine
import pymysql
import rds_config
import sys

s3_client = boto3.client('s3')

rds_host  = "apidb.cisebersdotq.us-east-1.rds.amazonaws.com"
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = create_engine('mysql+pymysql://{0}:{1}@{2}/{3}'.format(name, password, rds_host, db_name))
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()
    
logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")

def lambda_handler():
    conn.execute('SET FOREIGN_KEY_CHECKS = 0;')
    avro_records = []

    s3_client.download_file('backup-compnay-bucket', 'departments.avro','departments.avro')

    with open('departments.avro', 'rb') as fo:
        avro_reader = reader(fo)
        for record in avro_reader:
            avro_records.append(record)

    df_avro = pd.DataFrame(avro_records)
    df_avro.to_sql('api_departments', con=conn, if_exists='replace')

    avro_records = []

    s3_client.download_file('backup-compnay-bucket', 'jobs.avro','jobs.avro')

    with open('jobs.avro', 'rb') as fo:
        avro_reader = reader(fo)
        for record in avro_reader:
            avro_records.append(record)

    df_avro = pd.DataFrame(avro_records)
    df_avro.to_sql('api_jobs', con=conn, if_exists='replace')

    avro_records = []

    s3_client.download_file('backup-compnay-bucket', 'hired_employee.avro','hired_employee.avro')

    with open('hired_employee.avro', 'rb') as fo:
        avro_reader = reader(fo)
        for record in avro_reader:
            avro_records.append(record)

    df_avro = pd.DataFrame(avro_records)
    df_avro.to_sql('api_hired_employee', con=conn, if_exists='replace')
    conn.execute('SET FOREIGN_KEY_CHECKS = 1;')

    return "Backup items from RDS MySQL table"

print(lambda_handler())