from configparser import ConfigParser
from streamsets.sdk import ControlHub
from threading import Thread
from time import time, sleep

job_status_update_seconds = 10
max_wait_time_for_job_seconds = 10 * 60  # ten minutes


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
    def run_job_template(self, config):

        # Find the Job Template
        try:
            job_template = self.sch.jobs.get(job_id=config['job_template_id'])
        except Exception as e:
            print('Error: Job Template with ID \'' + config['job_template_id'] + '\' not found.')
            print(str(e))
            raise

        # Start the Job Template and return the list of Job Template Instances
        return self.sch.start_job_template(
            job_template,
            instance_name_suffix=config['instance_name_suffix'],
            parameter_name=config['parameter_name'],
            runtime_parameters=config['runtime_parameters'],
            attach_to_template=config['attach_to_template'],
            delete_after_completion=config['delete_after_completion'])





    # Get metrics for all Job Template Instances once they complete
    def get_metrics(self, job_template_instances):
        for job in job_template_instances:
            # Track each Job Template Instance in a separate thread to avoid blocking
            thread = Thread(target=self.get_metrics_for_job, args=(job,))
            thread.start()

        # Get metrics for a single Job Template Instance once it completes

    def get_metrics_for_job(self, job):
        start_seconds = time()
        elapsed_seconds = 0
        while elapsed_seconds < max_wait_time_for_job_seconds:
            elapsed_seconds = time() - start_seconds
            job.refresh()
            if job.status.status == 'INACTIVE' or job.status.status == 'INACTIVE_ERROR':
                break
            sleep(job_status_update_seconds)
        if job.status.status == 'INACTIVE':
            self.get_metrics_for_completed_job(job)
        else:
            self.handle_failed_job(job)
    @staticmethod
    def get_metrics_for_completed_job(job):
        job.refresh()
        metrics = job.metrics
        for metric in metrics:
            print('----------')
            print('Run Number: ' + str(metric.run_count))
            print('Input Count: ' + str(metric.input_count))
            print('Output Count: ' + str(metric.output_count))
            print('Total Error Count: ' + str(metric.total_error_count))
            print('----------')
            print('job history')
            h = job.history[0]
            print(h)
    def handle_failed_job(self, job):
        job.refresh()
        print('Job ' + job.job_name + ' has status ' + job.status.status )