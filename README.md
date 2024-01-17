# ETL Pipeline in AWS with Python

### Description:
This GitHub repository houses a comprehensive ETL (Extract, Transform, Load) pipeline implemented on Amazon Web Services (AWS) using the powerful programming language Python. The ETL process is a fundamental component of data engineering, allowing seamless extraction of data from various sources, transformation according to specific requirements, and loading into a target data store for further analysis.

### Key Features:
1. **AWS Integration**: Leverage the scalability and flexibility of AWS services, including S3 for storage, AWS Glue for data transformation, and Redshift or another suitable data warehouse for efficient data loading.
2. **Python Scripting**: The ETL pipeline is written in Python, a versatile and widely-used programming language. The code is designed for readability, maintainability, and extensibility.
3. **Modular Structure**: The repository adopts a modular structure for easy customization and expansion. Different components of the ETL process, such as extraction, transformation, and loading, are organized into distinct modules, enhancing code organization.
4. **Configurability**: Make the pipeline adaptable to different use cases with configuration files. Easily modify parameters such as data sources, transformation rules, and target destinations.
5. **Logging and Monitoring**: Implement robust logging and monitoring mechanisms to keep track of the ETL pipeline's performance and troubleshoot any issues that may arise during execution.
6. **Documentation**: Comprehensive documentation is provided to guide users through the setup, configuration, and customization of the ETL pipeline. This includes step-by-step instructions, code comments, and explanations of design choices.
7. **Sample Data**: Included sample datasets for testing and validating the ETL pipeline. Users can easily replace these datasets with their own sources to fit specific business requirements.

### Objective:
Whether you are a data engineer, scientist, or analyst, this repository offers a streamlined solution for building, deploying, and maintaining ETL pipelines on AWS, empowering you to efficiently manage and process your data at scale.

## AWS Architecture for ETL Pipeline
This architecture is designed to extract, transform, and load data using AWS services, including Amazon S3, AWS Glue, Amazon Redshift, and Amazon CloudWatch.

<picture>
<img alt="Shows the AWS Architecture Flowchart." src="https://github.com/lucassauaia/AWS-ETL-Pipeline-Python/blob/df7c42294d58e2472925f7ce799fac5e17bf80e7/assets/images/AWS%20Architecture.png">
</picture>

### Architecture Description:
1. **Amazon S3**: Used as source storage for the raw data.
2. **IAM**: Provides permissions so that AWS Glue can access necessary resources.
3. **Amazon Redshift**: Final storage database for the transformed data.
4. **Amazon CloudWatch**: Monitors and logs your AWS Glue job.
5. **AWS Glue**: Performs data extraction, transformation, and loading (ETL).

## Implementation
### Step 1: Amazon S3 Configuration
1. In the AWS console, navigate to Amazon S3.
2. Create a new bucket called `source-pipeline-etl`.
3. Upload the `WA_Fn-UseC_-Telco-Customer-Churn.csv` file into the created bucket.
### Step 2: Configuring the IAM Role
1. Access IAM (Identity and Access Management) in the AWS console.
2. Create a new role called `permission-pipeline-etl` that targets AWS Glue.
3. Add the following policies to the role:
   * AmazonS3ReadOnlyAccess
   * CloudWatchLogsFullAccess
   * AmazonRedshiftFullAccess
### Step 3: Configuring Amazon Redshift
1. In the AWS console, go to Amazon Redshift.
2. Create a new cluster called `redshift-pipeline` of type `dc2.large free tier`.
3. Configure the database called `dev` with the `admin` user. Set a password and store it securely.
4. On EC2, configure the security group to allow AWS Glue to connect to Redshift.
### Step 4: Amazon CloudWatch
CloudWatch will automatically create log groups for your AWS Glue job. There will be one group for error logs (`/aws-glue/python-jobs/error`) and another for output logs (`/aws-glue/python-jobs/output`).
### Step 5: Configuring the AWS Glue ETL Job
1. In the AWS console, go to AWS Glue and create a new ETL job called `etl-pipeline-to-redshift`.
2. Use the Script Editor to insert your locally developed ETL script.
3. Select the IAM Role `permission-pipeline-etl`.
4. Configure the job for Python, load common analysis libraries, set DPU to 1/16 and timeout to 5 minutes.
5. In advanced properties:
  *Set the script name to `transform-pipeline-etl.py`.
  *Add job parameters to connect to Redshift so that sensitive data is not in the code: Glue Job Parameters
6. Run the job manually. The expected output is: logs published in CloudWatch, creation of the `data_final` table in Redshift and insertion of data into the table. Output Logs Redshift Table

## Libraries Used
- **boto3**: Amazon SDK for Python that manipulates AWS resources.
- **BytesIO (from the io library)**: Interface for byte sequences that facilitates manipulation of S3 files as in-memory files.
- **psycopg2**: Library for connecting to PostgreSQL that allows interaction with Redshift instances.
- **sys**: Python's built-in library for interacting with the interpreter and passing command-line arguments.
- **getResolvedOptions (from the awsglue.utils library)**: AWS Glue SDK function that retrieves parameters from a GlueJob
