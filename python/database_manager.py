import psycopg2
from configparser import ConfigParser
import logging

logger = logging.getLogger(__name__)

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
                                       'delete_after_completion': row[6]}
                return job_template_config
            else:
                print('Error: No  job_template_config record found for name \'' + name + '\'')
                return None
        except Exception as e:
            logger.error("Error reading job_template_config from Postgres " + str(e))
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
            insert into streamsets.job_instance (
                job_instance_id           int not null primary key,
                job_run_id                int not null,
                job_template_id           int not null,
                user_id                   character varying    not null,
                engine_id                 character varying    not null,
                pipeline_id               character varying    not null,
                run_status                character varying    not null,
                input_record_count        int,
                output_record_count       int,
                error_record_count        int,
                error_message             character varying,
                start_time                timestamp,
                finish_time               timestamp,
            ) values ( 
                \'{}\',\'{}\',\'{}\',\'{}\',{},{},\'{}\',{},{},{},\'{}\',\'{}\'
            )
            """.format(
                metrics_data['user_id'],
                metrics_data['user_run_id'],
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
        except Exception as e:
            logger.error("Error writing job_run_metrics to Postgres " + str(e))
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
                user_id,
                user_run_id,
                job_template_id,
                job_id,
                run_number,
                successful_run,
                status,
                start_time
            ) values ( 
                \'{}\',\'{}\',\'{}\',\'{}\',{},{},\'{}\',\'{}\'
            )
            """.format(
                metrics_data['user_id'],
                metrics_data['user_run_id'],
                metrics_data['job_template_id'],
                metrics_data['job_id'],
                metrics_data['run_number'],
                metrics_data['successful_run'],
                metrics_data['status'],
                metrics_data['start_time']
            )
            cursor.execute(sql)
            conn.commit()
        except Exception as e:
            logger.error("Error writing job_run_metrics to Postgres " + str(e))
        finally:
            try:
                conn.close()
            except:
                pass
    # Gets SCH Job Template ID for source and destination
    def get_job_template_info (self, source, destination):
        conn = None
        try:
            conn = self.get_database_connection()
            cursor = conn.cursor()
            sql = """
           select t.sch_job_template_id,
                  t.delete_after_completion,
                  t.source_runtime_parameters,
                  t.destination_runtime_parameters,
                  t.source_connection_info,
                  t.destination_connection_info 
             from streamsets.job_template t, 
                streamsets.ingestion_pattern_job_template_relationship r,
                streamsets.ingestion_pattern p
             where p.source = '{}'
                and p.destination = '{}'
                and p.ingestion_pattern_id = r.ingestion_pattern_id
                and t.job_template_id = r.job_template_id
            """.format(source, destination).replace('\n', '')
            print(sql)
            cursor.execute(sql)
            result = cursor.fetchall()
            if result is not None and len(result) != 0:
                row = result[0]
                job_template_info = {'sch_job_template_id': row[0],
                'delete_after_completion': row[1],
                'source_runtime_parameters': row[2],
                'destination_runtime_parameters': row[3],
                'source_connection_info': row[4],
                'destination_connection_info': row[5]
            }
                return job_template_info
            else:
                print('Error: No  job_template record found for source \'{}\' and destination \'{}\'',format(source, destination))
            return None

        except Exception as e:
            logger.error("Error reading job_template from Postgres " + str(e))

        finally:
            try:
                conn.close()
            except:
                # Swallow any exceptions closing the connection
                pass