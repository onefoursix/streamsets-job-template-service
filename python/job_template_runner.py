from job_template_config_manager import JobTemplateConfigManager


def run_job_template(name):
    config_manager = JobTemplateConfigManager()
    job_template_config = config_manager.get_job_template_config(name)
    print(job_template_config)

run_job_template('files-to-gcp-prod-1')