import psycopg2
from configparser import ConfigParser


class DatabaseManager:
    def __init__(self):
        # Read database connection properties from ../database.ini file
        parser = ConfigParser()
        parser.read('../database.ini')
        self.db_config = parser['postgresql']

    # returns a database connection:
    def get_database_connection(self):
        db_config = self.db_config
        return psycopg2.connect(
            host=db_config['host'],
            port=db_config['port'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password'])

    # Get a Job Template Config record from the database by its unique name
    def get_job_template_config(self, name):
        conn = None
        try:
            conn = self.get_database_connection()
            cursor = conn.cursor()
            sql = 'select * from streamsets.job_template_config where name = \'' + name + '\''
            cursor.execute(sql)
            result = cursor.fetchall()
            if result is not None and len(result) != 0:
                row = result[0]
                job_template_config = {'id': row[0],
                                       'name': row[1],
                                       'job_template_id': row[2],
                                       'instance_name_suffix': row[3],
                                       'parameter_name': row[4],
                                       'attach_to_template': row[5],
                                       'delete_after_completion': row[6],
                                       'runtime_parameters': row[7]}
                return job_template_config
            else:
                print('Error: No  job_template_config record found for name \'' + name + '\'')
                return None
        finally:
            try:
                conn.close()
            except:
                # Swallow any exceptions closing the connection
                pass

    # Inserts a successful Job Metrics record into the database
    def write_job_metrics_record(self, metrics_data):
        conn = None
        try:
            conn = self.get_database_connection()
            cursor = conn.cursor()
            sql = """
            insert into streamsets.job_run_metrics (
                job_template_id,
                job_id,
                run_number,
                successful_run,
                status,
                input_count,
                output_count,
                error_count,
                start_time,
                finsh_time
            ) values ( 
                \'{}\',\'{}\',{},{},\'{}\',{},{},{},\'{}\',\'{}\'
            )
            """.format(
                metrics_data['job_template_id'],
                metrics_data['job_id'],
                metrics_data['run_number'],
                metrics_data['successful_run'],
                metrics_data['status'],
                metrics_data['input_count'],
                metrics_data['output_count'],
                metrics_data['error_count'],
                metrics_data['start_time'],
                metrics_data['finish_time']
            )
            cursor.execute(sql)
            conn.commit()

        finally:
            try:
                conn.close()
            except:
                pass
    # Inserts a failed Job run record into the database

    def write_failed_job_metrics_record(self, metrics_data):
        conn = None
        try:
            conn = self.get_database_connection()
            cursor = conn.cursor()
            sql = """
            insert into streamsets.job_run_metrics (
                job_template_id,
                job_id,
                run_number,
                successful_run,
                status,
                start_time
            ) values ( 
                \'{}\',\'{}\',{},{},\'{}\',\'{}\'
            )
            """.format(
                metrics_data['job_template_id'],
                metrics_data['job_id'],
                metrics_data['run_number'],
                metrics_data['successful_run'],
                metrics_data['status'],
                metrics_data['start_time']
            )
            cursor.execute(sql)
            conn.commit()

        finally:
            try:
                conn.close()
            except:
                pass
