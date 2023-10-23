from configparser import ConfigParser
from streamsets.sdk import ControlHub


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

    # Creates and starts one or more Job Template Instances
    def run_job_template(self, config):

        # Find the Job Template
        try:
            job_template = self.sch.jobs.get(job_id=config['job_template_id'])
        except Exception as e:
            print('Error: Job Template with ID \'' + config['job_template_id'] + '\' not found.')
            print(str(e))
            raise

        # Start the Job Template Instance(s)
        self.sch.start_job_template(
            job_template,
            instance_name_suffix=config['instance_name_suffix'],
            parameter_name=config['parameter_name'],
            runtime_parameters=config['runtime_parameters'],
            attach_to_template=config['attach_to_template'],
            delete_after_completion=config['delete_after_completion'])
