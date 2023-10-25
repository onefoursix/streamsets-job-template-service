from database_manager import DatabaseManager
from streamsets_manager import StreamSetsManager
import logging

import logging
logger = logging.getLogger(__name__)

def run_job_template(args: dict):

    try:
        user_id = args['user-id']
        user_run_id = args['user-run-id']
        job_template_config_name = args['job-template-config-name']

        # Get Job Template Config from the database
        config = DatabaseManager().get_job_template_config(job_template_config_name)

        # Get StreamSets Manager
        streamsets_manager = StreamSetsManager()

        # Start the Job Template
        job_template_instances = streamsets_manager.run_job_template(config)

        # Get metrics when Job(s) complete
        streamsets_manager.get_metrics(user_id, user_run_id, job_template_instances)

    except Exception as e:
        logger.error('Error running Job Template' + str(e))
        raise
