from job_template_config_manager import JobTemplateConfigManager
from streamsets_manager import StreamSetsManager


def run_job_template(name):

    try:
        # Get Job Template Config from Postgres
        config_manager = JobTemplateConfigManager()
        job_template_config = config_manager.get_job_template_config(name)

        # Get StreamSets Manager
        streamsets_manager = StreamSetsManager()

        # Run Job Template
        streamsets_manager.run_job_template(job_template_config)

        # Start the Job Template
        job_template_instances = streamsets_manager.run_job_template(job_template_config)

        # Wait for Job Template Instances to complete
        streamsets_manager.wait_for_completion(job_template_instances)

    except Exception as e:
        print('Error running Job Template' + str(e))
        raise


run_job_template('files-to-gcp-prod-1')
