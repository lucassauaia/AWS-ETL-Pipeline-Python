import pandas as pd  # For data manipulation
import boto3  # Importing boto3 allows Python developers to interact with AWS services like S3.
from io import BytesIO  # Allows handling bytes in memory as a "virtual file" for reading.
import psycopg2  # To connect and interact with the Redshift database
import sys  # Access to system functions and variables.
from awsglue.utils import getResolvedOptions  # Retrieves parameters defined in the GlueJob.

########## Extraction
print('Starting data extraction')
# Initializes the boto3 client to interact with the Amazon S3 service
s3 = boto3.client('s3')

# Defines the S3 bucket name where the CSV file is stored and the key of the object within the S3 bucket to be accessed
bucket_name = "source-pipeline-etl"
object_key = "Dataset.csv"

# Retrieving the CSV object from S3
response = s3.get_object(Bucket=bucket_name, Key=object_key)

# Reading the content of the obtained object into a temporary buffer.
buffer = BytesIO(response['Body'].read())

# Reading the buffer directly with pandas to obtain a DataFrame.
print(f'Starting reading data from the file {object_key} in the bucket {bucket_name}')
df = pd.read_csv(buffer)
print('Data read successfully')

########## Transformation
print('Starting data transformations')
# Requirement 1
df = df[['customerID', 'gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure']]
print('Requirement 1 DONE')
# Requirement 2
df['SeniorCitizen'] = df['SeniorCitizen'].replace({0: False, 1: True})
print('Requirement 2 DONE')
# Requirement 3
df['Partner'] = df['Partner'].replace({'Yes': True, 'No': False})
df['Dependents'] = df['Dependents'].replace({'Yes': True, 'No': False})
print('Requirement 3 DONE')
# Requirement 4
def classify_customers(tenure):
    if tenure <= 6:
        return 'new'
    elif tenure <= 12:
        return 'bronze'
    elif tenure <= 36:
        return 'silver'
    elif tenure <= 60:
        return 'gold'
    else:
        return 'platinum'
df['classification'] = df['tenure'].apply(classify_customers)
print('Requirement 4 DONE')
print(f'Viewing sample data to be inserted into Redshift \n {df.head()}')

# Limiting to 100 records to save processing time
df = df.head(100)

########## Load
print('Starting data loading into Redshift')

# Connection information for Redshift
args = getResolvedOptions(sys.argv, [
    'REDSHIFT_ENDPOINT',
    'REDSHIFT_DBNAME',
    'REDSHIFT_PORT',
    'REDSHIFT_USER',
    'REDSHIFT_PASSWORD'
])

redshift_host = args['REDSHIFT_ENDPOINT']
redshift_dbname = args['REDSHIFT_DBNAME']
redshift_port = args['REDSHIFT_PORT']
redshift_user = args['REDSHIFT_USER']
redshift_password = args['REDSHIFT_PASSWORD']

# Establishing a connection to the database using the psycopg2 library.
conn = psycopg2.connect(
    host=redshift_host,         # Database server address.
    dbname=redshift_dbname,     # Database name.
    user=redshift_user,         # User name for connection.
    password=redshift_password, # User password.
    port=redshift_port          # Connection port.
)

# Creating a cursor object that allows executing SQL commands in the database.
cursor = conn.cursor()

# SQL query to drop the 'final_data' table if it already exists in the database.
# This action is irreversible and, in production scenarios, may not be desired. It is only for didactic purposes.
drop_table_query = """
DROP TABLE IF EXISTS final_data;
"""

# Executing the drop command
cursor.execute(drop_table_query)

# SQL query to create a new table named 'final_data' with specific columns and types.
create_table_query = """
CREATE TABLE final_data (
    customerID VARCHAR(255),
    gender VARCHAR(50),
    SeniorCitizen BOOLEAN,
    Partner BOOLEAN,
    Dependents BOOLEAN,
    tenure INT,
    classification VARCHAR(50)
);
"""

# Executing the create table command
cursor.execute(create_table_query)

# Confirming (committing) the changes to the database
conn.commit()

# Inserting DataFrame data into the table, row by row
print('Inserting data into Redshift')
for index, row in df.iterrows():
    insert_query = """
    INSERT INTO final_data (
        customerID, gender, SeniorCitizen, Partner, Dependents, tenure, classification
    ) VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    cursor.execute(insert_query, tuple(row))
    conn.commit()

# Closing the cursor and the database connection to release resources.
cursor.close()
conn.close()

print(f'Data loading into Redshift completed successfully! {df.shape[0]} records were loaded into the table.')