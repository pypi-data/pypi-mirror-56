import logging
import time
import datetime

import googleapiclient.discovery

logger = logging.getLogger(__name__)

BIGGERQUERY_JOB_FAILURE_METRIC_TYPE = 'custom.googleapis.com/biggerquery_job_failure_count'
BIGGERQUERY_JOB_FAILURE_METRIC = {
        "type": BIGGERQUERY_JOB_FAILURE_METRIC_TYPE,
        "labels": [
            {
                "key": "job_id",
                "valueType": "STRING",
                "description": "Job UUID"
            }
        ],
        "metricKind": "CUMULATIVE",
        "valueType": "INT64",
        "unit": "items",
        "description": "Job failure counter",
        "displayName": "Job failure count"
    }


class MetricError(RuntimeError):
    pass


def format_rfc3339(datetime_instance=None):
    return datetime_instance.isoformat("T") + "Z"


def get_start_time():
    start_time = datetime.datetime.utcnow() - datetime.timedelta(minutes=5)
    return format_rfc3339(start_time)


def get_now_rfc3339():
    return format_rfc3339(datetime.datetime.utcnow())


def metric_exists(client, project_resource, metric_type):
    request = client.projects().metricDescriptors().list(
        name=project_resource,
        filter='metric.type=starts_with("{}")'.format(metric_type))
    response = request.execute()
    try:
        return response['metricDescriptors'] is not None
    except KeyError:
        logger.warning('Metric not found: {}'.format(metric_type))
        return False


def create_metric(client, project_resource, metric_descriptor):
    return client.projects().metricDescriptors().create(
        name=project_resource, body=metric_descriptor).execute()


def wait_for_metric(client, project_resource, metric_type):
    retries_left = 10
    while not metric_exists(client, project_resource, metric_type) and retries_left:
        logger.info('Waiting for metric: {}'.format(metric_type))
        time.sleep(1)
        retries_left -= 1


def increment_counter(client, monitoring_config, metric_type, job_id):
    start = get_now_rfc3339()
    end = get_now_rfc3339()
    timeseries_data = {
        "metric": {
            "type": metric_type,
            "labels": {
                "job_id": job_id
            }
        },
        "resource": {
            "type": 'cloud_composer_environment',
            "labels": {
                'project_id': monitoring_config.project_id,
                'location': monitoring_config.region,
                'environment_name': monitoring_config.environment_name
            }
        },
        "points": [
            {
                "interval": {
                    "startTime": start,
                    "endTime": end
                },
                "value": {
                    "int64Value": 1
                }
            }
        ]
    }

    request = client.projects().timeSeries().create(
        name=monitoring_config.project_resource, body={"timeSeries": [timeseries_data]})
    request.execute()


def increment_job_failure_count(monitoring_config, job_id):
    try:
        client = googleapiclient.discovery.build('monitoring', 'v3')
        if not metric_exists(client, monitoring_config.project_resource, BIGGERQUERY_JOB_FAILURE_METRIC_TYPE):
            create_metric(client, monitoring_config.project_resource, BIGGERQUERY_JOB_FAILURE_METRIC)
            wait_for_metric(client, monitoring_config.project_resource, BIGGERQUERY_JOB_FAILURE_METRIC_TYPE)
        increment_counter(client, monitoring_config, BIGGERQUERY_JOB_FAILURE_METRIC_TYPE, job_id)
    except Exception as e:
        raise MetricError('Cannot increment job failure count: ' + str(e))


class MonitoringConfig(object):
    def __init__(self, project_id, region, environment_name):
        self.project_resource = 'projects/{}'.format(project_id)
        self.project_id = project_id
        self.region = region
        self.environment_name = environment_name


def meter_job_run_failures(job, monitoring_config):
    original_run = job.run

    def metered_run(runtime):
        try:
            return original_run(runtime)
        except Exception as e:
            logger.error(str(e))
            increment_job_failure_count(monitoring_config, job.id)
            raise e

    job.run = metered_run
    return job