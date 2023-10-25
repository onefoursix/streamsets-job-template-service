from flask import Flask, request
import logging
import job_template_runner
import logging

log_file = '/tmp/streamsets-job-template-service.log'

# Create a logger
logger = logging.getLogger(__name__)
logging.basicConfig(filename=log_file,level=logging.INFO)

app = Flask(__name__)

def validate_request_data(json):
    if not (isinstance(json['user-id'], str) and len(json['user-id']) > 0):
        message = "Bad value for \'user-id\' arg"
        logger.error(message)
        raise Exception(message)
    if not (isinstance(json['user-run-id'], str) and len(json['user-run-id']) > 0):
        message = "Bad value for \'user-run-id\' arg"
        logger.error(message)
        raise Exception (message)
    if not (isinstance(json['job-template-config-name'], str) and len(json['job-template-config-name']) > 0):
        message = "Bad value for \'job-template-config-name\' arg"
        logger.error(message)
        raise Exception (message)

@app.route('/streamsets/job-template-runner', methods=['POST'])
def handle_job_template_runner_request():
    logger.info('handle_job_template_runner_request')
    try:
        validate_request_data(request.json)
        job_template_runner.run_job_template(request.json)
        return {"status": "OK"}
    except Exception as e:
        return {"status": "There was an error: " + str(e)}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8888)
