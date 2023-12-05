from database_manager import DatabaseManager
from streamsets_manager import StreamSetsManager

import logging
logger = logging.getLogger(__name__)


def get_template_for_source_and_target(source, target):
    # A single hardcoded example
    if source == 'http' and target == 'gcs':
        return 'http-to-gcs'


def run_job_template(request: dict):

    try:

        # Get Database Manager
        db = DatabaseManager()

        # Get appropriate template for source and target types:
        template_name = get_template_for_source_and_target(request['source-type'], request['target-type'])

        # Get Job Template Config from the database
        template = DatabaseManager().get_job_template_config(template_name)

        # Get StreamSets Manager
        streamsets_manager = StreamSetsManager()

        # Start the Job Template
        job_template_instances = streamsets_manager.run_job_template(template, request)

        # Get metrics when Job(s) complete
        streamsets_manager.get_metrics(request['user-id'], request['user-run-id'], job_template_instances)

    except Exception as e:
        logger.error('Error running Job Template' + str(e))
        raise
