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
)

