from postgres_manager import PostgresManager
from streamsets_manager import StreamSetsManager


def run_job_template(name):

    try:
        # Get Job Template Config from Postgres
        postgres = PostgresManager()
        job_template_config = postgres.get_job_template_config(name)

        # Get StreamSets Manager
        streamsets_manager = StreamSetsManager()

        # Start the Job Template
        job_template_instances = streamsets_manager.run_job_template(job_template_config)

        # Get metrics when Job(s) complete
        streamsets_manager.get_metrics(job_template_instances)

    except Exception as e:
        print('Error running Job Template' + str(e))
        raise


run_job_template('oracle-to-adls-prod-1')
# run_job_template('files-to-gcp-prod-1')
