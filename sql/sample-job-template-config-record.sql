insert into streamsets.job_template_config (
  id,
  name,
  job_template_id,
  instance_name_suffix,
  parameter_name,
  attach_to_template,
  delete_after_completion
) values (
  1,
  'http-to-gcs',
  'c09f728a-2a73-4c7e-b735-2512039a9e6b:8030c2e9-1a39-11ec-a5fe-97c8d4369386',
  'PARAM_VALUE',
  'CITY',
  true,
  false
)