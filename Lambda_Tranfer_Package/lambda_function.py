import boto3
import logging
import csv
import rds_config
import pymysql
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
    
    bucket = event['detail']['bucket']['name']
    object = event['detail']['object']['key']
    
    csv_file_obj = s3_client.get_object(Bucket=bucket, Key=object)
    lines = csv_file_obj['Body'].read().decode('utf-8').split('\n')
        
    with conn.cursor() as cur:
        results = []
        if object.startswith('departments'):
            for row in csv.DictReader(lines,fieldnames=['id','department']):
                results.append(row)
        
            for line in results:
                cur.execute('insert into api_departments (id, department) values({0}, "{1}")'.format(line['id'],line['department']))
        elif object.startswith('jobs'):
            for row in csv.DictReader(lines,fieldnames=['id','job']):
                results.append(row)
                
            for line in results:
                cur.execute('insert into api_jobs (id, job) values({0}, "{1}")'.format(line['id'],line['job']))
        elif object.startswith('hired_employees'):
            for row in csv.DictReader(lines,fieldnames=['id','name','datetime','department_id','job_id']):
                results.append(row)
                
            for line in results:
                cur.execute('insert into api_hired_employee (id, name, datetime, department_id, job_id) values({0}, "{1}", "{2}", {3}, {4})'.format(line['id'],line['name'],line['datetime'],line['department_id'],line['job_id']))
            
    conn.commit()

    return "Added items from RDS MySQL table"
    