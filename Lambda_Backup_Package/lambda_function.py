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
    conn = pymysql.connect(host=rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()
    
logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")

def lambda_handler(event, context):    
    data = pd.read_sql("select * from Company_db.api_hired_employee", conn)

    schema = {
        'doc': 'BACKUP',
        'name': 'BACKUP',
        'namespace': 'company',
        'type': 'record',
        'fields': [
            {'name': 'id', 'type': 'int'},
            {'name': 'name', 'type': 'string'},
            {'name': 'datetime', 'type': 'string'},
            {'name': 'department_id_id', 'type': 'int'},
            {'name': 'job_id_id', 'type': 'int'}
        ]
    }

    parsed_schema = parse_schema(schema)

    data['datetime'] = data['datetime'].values.astype(str)
    records = data.to_dict('records')

    with open('hired_employee.avro', 'wb') as out:
        writer(out, parsed_schema, records)

    s3_client.upload_file('hired_employee.avro', 'backup-compnay-bucket', 'hired_employee.avro')

    data = pd.read_sql("select * from Company_db.api_departments", conn)

    schema = {
        'doc': 'Database backup',
        'name': 'Backup',
        'namespace': 'test',
        'type': 'record',
        'fields': [
            {'name': 'id', 'type': 'int'},
            {'name': 'department', 'type': 'string'}
        ]
    }

    parsed_schema = parse_schema(schema)

    records = data.to_dict('records')

    with open('departments.avro', 'wb') as out:
        writer(out, parsed_schema, records)

    s3_client.upload_file('departments.avro', 'backup-compnay-bucket', 'departments.avro')

    data = pd.read_sql("select * from Company_db.api_jobs", conn)

    schema = {
        'doc': 'BACKUP',
        'name': 'BACKUP',
        'namespace': 'company',
        'type': 'record',
        'fields': [
            {'name': 'id', 'type': 'int'},
            {'name': 'job', 'type': 'string'}
        ]
    }

    parsed_schema = parse_schema(schema)

    records = data.to_dict('records')

    with open('jobs.avro', 'wb') as out:
        writer(out, parsed_schema, records)

    s3_client.upload_file('jobs.avro', 'backup-compnay-bucket', 'jobs.avro')

    return "Backup items from RDS MySQL table"
