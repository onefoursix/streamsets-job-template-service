from configparser import ConfigParser
from streamsets.sdk import ControlHub
from threading import Thread
from time import time, sleep

job_status_update_seconds = 10
max_wait_time_for_job_seconds = 10 * 60 # ten minutes


def get_metrics_for_completed_job(self, job):
    pass


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

    # Wait for a Job Template Instance to complete
    def wait_for_job_to_complete(self, job):
        start_seconds = time()
        elapsed_seconds = 0
        while elapsed_seconds < max_wait_time_for_job_seconds:
            elapsed_seconds =  time() - start_seconds
            job.refresh()
            job_status = job.status.status
            if job_status == 'INACTIVE':
                get_metrics_for_completed_job(self, job)

        print('Job status is \'' + job_status + '\'')
        print("Job" + str(job))

    # Wait for all Job Template Instances to complete
    def wait_for_all_instances_to_complete(self, job_template_instances):
        for job in job_template_instances:
            # Track each Job Template Instance in a separate thread to avoid blocking
            thread = Thread(target = self.wait_for_job_to_complete, args = (job,))
            thread.start()
            thread.join()

