from flask import Flask, request

import job_template_runner

app = Flask(__name__)

@app.route('/streamsets/job-template-runner', methods=['POST'])
def handle_job_template_runner_request():
    try:
        job_template_name = request.json['job-template-name']
        job_template_runner.run_job_template(job_template_name)
        return {"status": "OK"}
    except Exception as e:
        return {"status": "There was an error: " + str(e)}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8888)