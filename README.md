# Data Pipeline and Ochestration using GCP, Kestra, Terraform, DBT and visualization with Looker
Introducing a Data Pipeline Project that integrates Airflow for Data Orchestration <br>

### Technologies used
- <b>Kestra</b>: Kestra is an open-source platform for authoring, scheduling and monitoring data and computing workflows. For this project it was used to manage data extraction. transformation and loading process<br><br>
- <b>Big Query</b>: This is a cloud-based data warehousing platform for data storage and analytics purpose. For this project it was used to query datasets loaded automatically from S3<br><br>
- <b>GCP Bucket</b>: This is a highly scalable object storage service that stores data as objects within buckets. It is commonly used to store and distribute large media files, data backups and static website files. For this project it is used to store data scraped from target website. <br><br>
- <b>DBT</b>: This is a message queuing service. It exchanges and stores messages between software components. The service adds the messages in a queue. Users or services pick up the messages from the queue. Once processed the messages gets deleted from the queue. In this project it was used to receive notifications from S3 to an SQS queue to be read by the Snowflake server. <br><br>



## DBT Lineage
<img src="readme_images/architecture.png">
<br>

### Languages used
- Python
<br><br>

### Datasets
Data was extracted from <a href="https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page">NYU Taxi dataset </a>

### Getting Started
1. Create EC2 Instance (AWS Ubuntu Server) with at least 4gb RAM as requested by airflow installation requirements - preferable t3.medium<br>
<img src='readme_images/instance.png'><br><br>
    
2. Install Airflow and other libraries on ec2 Instance. Use commands <a href="https://github.com/priye-1/airflow_data_pipeline/blob/master/ubuntu_commands.sh">here</a> to install dependencies and start airflow server. Clone dags from this repository into your ubuntu directory using git. This will allow you to access the scraper and dag code on your server. Airflow UI can then be accessed using this url format - `http://<public dns address>:8080`<br>
<img src='readme_images/airflow.png'><br>

3. Create a snowflake account <a href="https://signup.snowflake.com/">here</a> , also create database, staging environment for incoming files on snowflake, table and pipe to copy data from stage to snowflakes table. Data pipelines can leverage Snowpipe to continously load micro-batches of data into tables for automated tasks. Follow commands <a href="https://github.com/priye-1/airflow_data_pipeline/blob/master/snowflakes_queries.sql">here</a> to create database, tables, etc.
<br><br>

4. Create S3 Bucket and IAM role to enable access to s3 from any instance, take note of the AWS key and secret key <br>
<img src='readme_images/s3.png'><br><br>

5. Set up AWS SQS for all bucket create operations<br> To enable the bucket to notify Snowpipe when new data arrives. This can be done by executing the query “show pipes;” in snowflakes worksheet, copying the notification_channel(ARN) value from the newly created pipe, and pasting it into the AWS SQS.
<img src='readme_images/event.png'><br><br>

6. Trigger dag manually from the UI and access Snowflake worksheet to preview data, with time the number of rows increases if airflow task is set to run on a schedule.<br>
<img src='readme_images/pipeline.png'>
<br>
<img src='readme_images/snowflakes.png'>
<br>

#### Pipeline Flow
start Airflow server-> Trigger data crawler Dag -> Crawler starts -> loads data into s3 ->   snowpipe loads data into table from s3 <br><br>

#### Necessary Files
1. Ubuntu commands for Airflow setup can be found <a href="https://github.com/priye-1/airflow_data_pipeline/blob/master/ubuntu_commands.sh">here</a>
2. Airflow and scrapy code can be found  <a href="https://github.com/priye-1/airflow_data_pipeline/tree/master/dags">here</a> This should run in your environment if set up correctly
3. Snowflake queries can be found <a href="https://github.com/priye-1/airflow_data_pipeline/blob/master/snowflakes_queries.sql">here</a>


### Dashboard
<li><a href="https://lookerstudio.google.com/reporting/b5bae0e4-6b63-4e86-8b60-0a4374d01e45">Dashboard with Looker</a></li>
