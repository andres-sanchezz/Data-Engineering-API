# Data-Engineering-API

A Rest API was created to solve some data transactions from a company using the python framework django. It solves the requirements mentioned in Proporsal For Coding Challenge this way:

* Move historic data to new database
For this requirements it was used AWS S3, Lambda and Stepfunctions to create a flow that would be triggered when csv files with hitoric data where uploaded into a specific S3 Bucket to insert the data using Lambda functions automaticlly.
**Bucket to recieve historic data**
![image](https://user-images.githubusercontent.com/30332010/190576367-832b0e19-15a5-4a7c-96cb-f7ef3ef1871d.png)
**Stepfunction to execute the flow**
![image](https://user-images.githubusercontent.com/30332010/190576580-240ec41c-e692-4e3f-afd7-facd3bf37f7c.png)
**Lambda function to perform data transfer**
![image](https://user-images.githubusercontent.com/30332010/190576795-c029e064-6504-4fb1-b88f-2e41ae8a86a7.png)

* Create API Rest to recieve new data
It was created by using the python framework django, developing the necesary models, views, and url's for the services provided by an EC2 instance with server running on port 8000, connecting to the created database on AWS RDS, with the following methods:
1. Get /api/employees/<string:table> which allows to perform a query to get every element in a specific table.
2. Post /api/employees/ which allows you to insert new batch data to any table in database, recieving the data with the following structure:
{
  "destination_table": <"hired_employees", "departments", "jobs">,
  "data": [
    {
      "field": "value"
    }
  ]
}
This method takes into account the data rules defined in the problem.

* Feature for Backup in AVRO format
This feature was developed using AWS Lambda functions due to its sporadic executions, so it takes database information, transform it to AVRO format and upload the files into an AWS Bucket.

* Feature for Restore tables from AVRO format
This feature was developed using AWS Lambda functions due to its sporadic executions, so it takes files in AVRO format from an AWS Bucket, and transforms it to insert the data into database tables.
**Bucket for saving and recover Backup**
![image](https://user-images.githubusercontent.com/30332010/190580079-f7f24ce7-113d-4dd9-99e6-cb49cea14591.png)
