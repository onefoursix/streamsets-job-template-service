## streamsets-job-template-service
This project provides an example of how to use the [StreamSets Platform SDK](https://docs.streamsets.com/platform-sdk/latest/index.html) to parameterize and start Job Template instances based on settings in a PostgreSQL database.  A REST API service wrapper is also provided.


### Prerequisites

- Python 3.8+

- Psycopg (PostgreSQL database adapter for Python - see https://pypi.org/project/psycopg2/)

- StreamSets Platform SDK for Python v6.0.1+

- StreamSets Platform [API Credentials](https://docs.streamsets.com/portal/platform-controlhub/controlhub/UserGuide/OrganizationSecurity/APICredentials_title.html#concept_vpm_p32_qqb) for a user with permissions to start Jobs 

### Configuration Details

- Clone this project to your local machine

- Create the PostgreSQL user, schema, and tables by executing the <code>sql/postgres.sql</code> script against your PostgresSQL database. This will create these two tables in the <code>streamsets</code> schema:
  - <code>job_template_config</code>
  
  - <code>job_metrics</code>


- Create a file named <code>postgres.ini</code> at the root of your local project directory with the following entries, with values for the user and password just created:
```
[postgresql]
host=localhost
port=5432
database=postgres
user=streamsets
password=streamsets
```

- Create or select an existing parameterized pipeline and Job Template in Control Hub

- Execute a SQL statement like this to insert an entry into the <code>job_template_config</code> table for the Job Template:
```
insert into streamsets.job_template_config (
  id,
  name,
  job_template_id,
  instance_name_suffix,
  parameter_name,
  attach_to_template,
  delete_after_completion,
  runtime_parameters
) values (
  1,
  'files-to-gcp-prod-1',
  'fb4d0b8a-8c49-45ff-ad64-62c231924352:8030c2e9-1a39-11ec-a5fe-97c8d4369386',
  'PARAM_VALUE',
  'FILE_PICKUP_DIR',
  true,
  false,
  '[
      {
        "FILE_PICKUP_DIR": "/Users/mark/data/json",
        "FILE_NAME_PATTERN": "*.json",
        "GCS_CONNECTION": "9c960db9-7904-47c4-bbc8-4c95dcf9c959:8030c2e9-1a39-11ec-a5fe-97c8d4369386",
        "GCS_BUCKET": "146_gcs_bucket",
        "GCS_DIRECTORY": "files"
      }
  ]'
)
```