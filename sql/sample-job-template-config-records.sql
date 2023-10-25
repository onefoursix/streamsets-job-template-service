insert into streamsets.job_template_config values (
  1,
  'files-to-gcp-prod-1',
  'fb4d0b8a-8c49-45ff-ad64-62c231924352:8030c2e9-1a39-11ec-a5fe-97c8d4369386',
  'PARAMETER',
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

insert into streamsets.job_template_config values (
  2,
  'oracle-to-adls-prod-1',
  '187cba47-bef6-474e-882d-8f4445a66f5e:8030c2e9-1a39-11ec-a5fe-97c8d4369386',
  'PARAM_VALUE',
  'ORACLE_TABLE_PATTERN',
  true,
  false,
  '[
    {
      "ORACLE_CONNECTION": "86a76b7c-0ad9-4da4-8e48-3be048593c40:8030c2e9-1a39-11ec-a5fe-97c8d4369386",
      "ADLS_CONNECTION": "0a13edd2-d12d-41a1-be13-3da331d87820:8030c2e9-1a39-11ec-a5fe-97c8d4369386",
      "ORACLE_TABLE_PATTERN": "EMPLOYEE"
    },
    {
      "ORACLE_CONNECTION": "86a76b7c-0ad9-4da4-8e48-3be048593c40:8030c2e9-1a39-11ec-a5fe-97c8d4369386",
      "ADLS_CONNECTION": "0a13edd2-d12d-41a1-be13-3da331d87820:8030c2e9-1a39-11ec-a5fe-97c8d4369386",
      "ORACLE_TABLE_PATTERN": "TAXI_TRIPS"
    }
  ]'
)