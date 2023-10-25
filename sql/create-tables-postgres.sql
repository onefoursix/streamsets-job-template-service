create user streamsets with password 'streamsets';

create schema streamsets authorization streamsets;

create table streamsets.job_template_config(
  id                        bigint               not null primary key,
  name                      character varying    not null,
  job_template_id           character varying    not null,
  instance_name_suffix      character varying    not null, 
  parameter_name            character varying    null,   
  attach_to_template        boolean              not null, 
  delete_after_completion   boolean              not null, 
  runtime_parameters        jsonb                not null,
  CONSTRAINT name_unique UNIQUE (name)
);

create table streamsets.job_run_metrics (
  job_template_id           character varying    not null,
  job_id                    character varying    not null,
  run_number                bigint               not null,
  successful_run            boolean              not null,
  status                    character varying    not null,
  input_count               bigint,
  output_count              bigint,
  error_count               bigint,
  start_time                timestamp,
  finsh_time                timestamp
);

grant all on streamsets.job_template_config to streamsets;

grant all on streamsets.job_run_metrics to streamsets;

