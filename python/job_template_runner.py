from database_manager import DatabaseManager
from streamsets_manager import StreamSetsManager


def run_job_template(job_template_name):

    try:
        # Get Job Template Config from the database
        job_template_config = DatabaseManager().get_job_template_config(job_template_name)

        # Get StreamSets Manager
        streamsets_manager = StreamSetsManager()

        # Start the Job Template
        job_template_instances = streamsets_manager.run_job_template(job_template_config)

        # Get metrics when Job(s) complete
        streamsets_manager.get_metrics(job_template_instances)

    except Exception as e:
        print('Error running Job Template' + str(e))
        raise
