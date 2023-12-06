from configparser import ConfigParser
from streamsets.sdk import ControlHub
from threading import Thread
from time import time, sleep
from datetime import datetime
from database_manager import DatabaseManager
import logging

logger = logging.getLogger(__name__)

# How often to check for updated Job Status
job_status_update_seconds = 10

# How long to wait for a JOb to finish. Jobs that take longer
# than this amount of time will be considered to have failed.
max_wait_time_for_job_seconds = 4 * 60 * 60  # four hours


class StreamSetsManager:
    def __init__(self):
        # Read streamsets connection properties from ../streamsets.ini file
        parser = ConfigParser()
        parser.read('../streamsets.ini')
        self.streamsets_config = parser['streamsets']
        streamsets_config = self.streamsets_config

        # Connect to Control Hub
        self.sch = ControlHub(
            credential_id=streamsets_config['cred_id'],
            token=streamsets_config['cred_token'])

    # Starts a Job Template and returns a list of Job Template Instances
    def run_job_template(self, job_template_info, request):

        # Find the Job Template
        job_template_id = job_template_info['sch_job_template_id']
        try:
            job_template = self.sch.jobs.get(job_id=job_template_id)
            print('Found Job template \'{}\''.format(job_template.job_name))
        except Exception as e:
            logger.error('Error: Job Template with ID \'' + job_template_id+ '\' not found.' + str(e))
            raise

        # Start the Job Template using the runtime parameters in the request
        return self.sch.start_job_template(
            job_template,
            runtime_parameters=request['runtime-parameters'],
            instance_name_suffix='TIME_STAMP',
            attach_to_template=True, #job_template_info['attach_to_template'],
            delete_after_completion=job_template_info['delete_after_completion'])

    # Get metrics for all Job Template Instances once they complete
    def get_metrics(self, user_id, user_run_id, job_template_instances):
        for job in job_template_instances:
            # Track each Job Template Instance in a separate thread to avoid blocking
            thread = Thread(target=self.wait_for_job_completion_and_get_metrics,
                            args=(user_id, user_run_id, job,))
            thread.start()

    # Waits for Job to complete before getting its metrics
    def wait_for_job_completion_and_get_metrics(self, user_id, user_run_id, job):
        start_seconds = time()
        elapsed_seconds = 0
        while elapsed_seconds < max_wait_time_for_job_seconds:
            elapsed_seconds = time() - start_seconds
            job.refresh()
            if job.status.status == 'INACTIVE' or job.status.status == 'INACTIVE_ERROR':
                break
            sleep(job_status_update_seconds)

        self.write_metrics_for_job(user_id, user_run_id, job)

    @staticmethod
    def write_metrics_for_job(user_id, user_run_id, job):

        metrics_data = {'user_id': user_id, 'user_run_id': user_run_id}

        job.refresh()

        status = job.status.status

        metrics = job.metrics[0]
        history = job.history[0]

        metrics_data['status'] = status
        metrics_data['job_template_id'] = job.template_job_id
        metrics_data['job_id'] = job.job_id
        metrics_data['run_number'] = metrics.run_count
        metrics_data['start_time'] = datetime.fromtimestamp(history.start_time / 1000.0).strftime("%Y-%m-%d %H:%M:%S")

        # If the Job failed
        if status != 'INACTIVE':
            metrics_data['successful_run'] = False
            DatabaseManager().write_failed_job_metrics_record(metrics_data)

        # If the Job completed successfully
        else:
            metrics_data['successful_run'] = True
            metrics_data['input_count'] = metrics.input_count
            metrics_data['output_count'] = metrics.output_count
            metrics_data['error_count'] = metrics.total_error_count
            metrics_data['finish_time'] = datetime.fromtimestamp(history.finish_time / 1000.0).strftime("%Y-%m-%d %H:%M:%S")
            DatabaseManager().write_job_metrics_record(metrics_data)
