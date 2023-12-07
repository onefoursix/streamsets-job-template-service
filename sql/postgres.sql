create user streamsets with password 'streamsets';

create schema streamsets authorization streamsets;

create table streamsets.job_template(
  job_template_id                     int                  not null primary key,
  sch_job_template_id                 character varying    not null,
  delete_after_completion             boolean              not null,
  source_runtime_parameters           jsonb,
  destination_runtime_parameters      jsonb,
  source_connection_info              jsonb,
  destination_connection_info         jsonb,
  create_timestamp                    timestamp            not null
);

grant all on streamsets.job_template to streamsets;


create table streamsets.ingestion_pattern(
  ingestion_pattern_id              int                  not null primary key,
  pattern_name                      character varying    not null,
  source                            character varying    not null,
  destination                       character varying    not null,
  create_timestamp                  timestamp            not null
);  

grant all on streamsets.ingestion_pattern to streamsets;


create table streamsets.ingestion_pattern_job_template_relationship(
  rel_id                            int                  not null primary key,
  ingestion_pattern_id              int                  not null,
  job_template_id                   int                  not null,
  schedule                          character varying,
  CONSTRAINT ingestion_pattern_id
      FOREIGN KEY(ingestion_pattern_id)
    REFERENCES streamsets.ingestion_pattern(ingestion_pattern_id),
  CONSTRAINT job_template_id
      FOREIGN KEY(job_template_id)
    REFERENCES streamsets.job_template(job_template_id)
);

grant all on streamsets.ingestion_pattern_job_template_relationship to streamsets;


create table streamsets.job_instance (
  job_instance_id           int not null primary key,
  job_run_id                int not null,
  job_template_id           int not null,
  user_id                   character varying    not null,
  engine_id                 character varying    not null,
  pipeline_id               character varying    not null,
  run_status                character varying    not null,
  input_record_count        int,
  output_record_count       int,
  error_record_count        int,
  error_message             character varying,
  start_time                timestamp,
  finish_time                timestamp,
  CONSTRAINT job_template_id
      FOREIGN KEY(job_template_id) 
    REFERENCES streamsets.job_template(job_template_id)
);

grant all on streamsets.job_instance to streamsets;



insert into streamsets.ingestion_pattern (
  ingestion_pattern_id,
  pattern_name,
  source,
  destination,
  create_timestamp
)
 values(1000, 'http-to-gcs', 'http','gcs', CURRENT_TIMESTAMP);

insert into streamsets.job_template(
  job_template_id,
  sch_job_template_id,
  delete_after_completion,
  source_runtime_parameters,
  destination_runtime_parameters,
  source_connection_info,
  destination_connection_info,
  create_timestamp
  ) values (
    5000,
    'c09f728a-2a73-4c7e-b735-2512039a9e6b:8030c2e9-1a39-11ec-a5fe-97c8d4369386',
    false,
    '{}',
    '{}',
    '{}',
    '{}',
    CURRENT_TIMESTAMP
);


insert into streamsets.ingestion_pattern_job_template_relationship (
  rel_id,
  ingestion_pattern_id,
  job_template_id,
  schedule
) values (
    100,
    1000,
    5000,
   ''
);


