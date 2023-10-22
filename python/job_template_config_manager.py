import psycopg2
from configparser import ConfigParser




class JobTemplateConfigManager:
    def __init__(self):
        # Read database connection properties from ../postgres.ini file
        parser = ConfigParser()
        parser.read('../postgres.ini')
        self.db_config = parser['postgresql']

    # returns a Postgres connection:
    def get_postgres_connection(self):
        db_config = self.db_config
        return psycopg2.connect(
            host=db_config['host'],
            port=db_config['port'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password'])

    # Get a Job Template Config record from postgres by its unique name
    def get_job_template_config(self, name):
        conn = None
        try:
            conn = self.get_postgres_connection()
            cursor = conn.cursor()
            sql = 'select * from streamsets.job_template_config where name = \'' + name + '\''
            cursor.execute(sql)
            result = cursor.fetchall()
            if result != None and len(result) != 0:
                row = result[0]
                job_template_config = {}
                job_template_config['id'] = row[0]
                job_template_config['name'] = row[1]
                job_template_config['job_template_id'] = row[2]
                job_template_config['instance_name_suffix'] = row[3]
                job_template_config['parameter_name'] = row[4]
                job_template_config['attach_to_template'] = row[5]
                job_template_config['delete_after_completion'] = row[6]
                job_template_config['runtime_parameters'] = row[7]
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






