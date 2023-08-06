import os
import time
import logging

import requests

"""
suppress info and debug logging from the requests library.
It complains about python 2.6 not being able to create
secure connections, but as we are upgrading to Centos7/Python 2.7
then we aren't worried.
"""
logging.getLogger("requests").setLevel(logging.WARNING)
try:
    requests.packages.urllib3.disable_warnings()
except Exception as e:
    print("Could not suppress requests error")

server = None
user = None
password = None

log = logging.getLogger('csa_api')
log.setLevel(logging.WARNING)

MAX_RETRIES = 50


class Url(object):
    PIPELINE_STEP_RESERVE = '/csa/api/sample_pipeline_steps/reserve.json'
    PIPELINE_STEP_RESERVE_BATCH = '/csa/api/sample_pipeline_steps/reserve_batch.json'
    COMPLETE_PIPELINE_STEP = '/csa/api/sample_pipeline_steps/{id}/complete.json'
    FAIL_PIPELINE_STEP = '/csa/api/sample_pipeline_steps/{id}/fail.json'
    ORGANIZATION_RESOURCE = '/csa/apiorganizations/{id}.json'
    SAMPLE_DATA_SETS = '/csa/api/sample_data_sets.json'
    SAMPLE_DATA_SET = '/csa/api/sample_data_sets/by_pn/{id}.json'
    SUBJECTS = '/csa/api/subjects/{id}.json'
    REFERENCE_DATA_VERSIONS = '/csa/api/reference_data_versions'
    REFERENCE_DATA_VERSION = '/csa/api/reference_data_versions/by_path/{id}.json'
    PROJECTS_SCOPE = '/csa/api/projects.json?scope={scope}'
    PROJECT_RETRIEVAL = '/csa/api/projects/{project_name}.json'
    SAMPLE_ORG_EXTID = '/csa/api/organizations/{org_key}/sample_data_sets/by_extid/{extid}.json'


class Auth(object):
    CREDENTIALS_BASE = '/credentials.json'
    GET_CREDENTIALS = CREDENTIALS_BASE + (
        '?find[project_key]={project_key}' '&find[service]={service}&find[lookup_key]={lookup_key}'
    )
    ADD_CREDENTIALS = CREDENTIALS_BASE

    @staticmethod
    def build_filter_string(**kwargs):
        filter_format = 'find[%(key)s]=%(val)s&'
        filter_str = ""
        for (key, val) in kwargs.items():
            filter_str += filter_format % (dict(key=key, val=val))
        return "%s?%s" % (Auth.CREDENTIALS_BASE, filter_str)

    @staticmethod
    def get_credentials_for_id(id):
        return


def configure(_server, _user, _password):
    global server, user, password
    server = _server
    user = _user
    password = _password


def configure_from_environment():
    csa_api_endpoint = os.environ.get('CSA_API_ENDPOINT')
    if csa_api_endpoint is None:
        raise ValueError("Expected 'CSA_API_ENDPOINT' to be set")

    csa_api_user = os.environ.get('CSA_API_USER')
    if csa_api_user is None:
        raise ValueError("Expected 'CSA_API_USER' to be set")

    csa_api_password = os.environ.get('CSA_API_PASSWORD')
    if csa_api_password is None:
        raise ValueError("Expected 'CSA_API_PASSWORD' to be set")

    configure(csa_api_endpoint, csa_api_user, csa_api_password)


def _get(uri):
    """
    Thin wrapper for requests.get to get logs, json output and proper exceptions.
    :param uri:
    :return: response.json() - or raises Exception
    """
    if server is None or user is None or password is None:
        raise Exception("Server, user or password for CSA Api is not configured")
    log.debug("Calling '%s' to get credentials for project", uri)
    resp = requests.get(uri, auth=(user, password))
    log.debug("CSA API responded to credentials call with content '%s'", resp.content)
    resp.raise_for_status()
    return resp.json()


def reserve_sample_pipeline_step(hostname, pid, url, message):
    uri = server + Url.PIPELINE_STEP_RESERVE
    log.info("Calling '%s' to reserve step..", uri)
    response = requests.put(
        uri,
        auth=(user, password),
        json={
            "sample_pipeline_step": {
                "worker_name": hostname,
                "worker_pid": pid,
                "worker_job_url": url,
                "worker_message": message,
            }
        },
    )
    response.raise_for_status()

    try:
        return response.json()
    except Exception:
        log.exception("could not parse JSON response from server while reserving pipeline step")
        raise


def reserve_sample_pipeline_steps(hostname, pid, url, message):
    uri = server + Url.PIPELINE_STEP_RESERVE_BATCH
    log.info("Calling '%s' to reserve step..", uri)
    response = requests.put(
        uri,
        auth=(user, password),
        json={
            "sample_pipeline_step": {
                "worker_name": hostname,
                "worker_pid": pid,
                "worker_job_url": url,
                "worker_message": message,
            }
        },
    )
    response.raise_for_status()

    try:
        return response.json()
    except Exception:
        log.exception("could not parse JSON response from server while reserving pipeline step")
        raise


def complete_sample_pipeline_step(id, hostname, pid, url, message, retry=0):
    uri = server + Url.COMPLETE_PIPELINE_STEP.format(id=id)
    log.info("Calling '%s' to complete step", uri)
    response = requests.put(
        uri,
        auth=(user, password),
        json={
            "sample_pipeline_step": {
                "worker_name": hostname,
                "worker_pid": pid,
                "worker_job_url": url,
                "worker_message": message,
            }
        },
    )

    if response.ok:
        return response.json()
    else:
        if retry > MAX_RETRIES:
            response.raise_for_status()
        # sleep for as many seconds as we have retried so that we do not flood the server
        time.sleep(retry)
        return complete_sample_pipeline_step(id, hostname, pid, url, message, retry + 1)


def fail_sample_pipeline_step(id, hostname, pid, url, message, retry=0):
    uri = server + Url.FAIL_PIPELINE_STEP.format(id=id)
    log.warn("Calling '%s' to mark step as failed with message %s", uri, message)
    response = requests.put(
        uri,
        auth=(user, password),
        json={
            "sample_pipeline_step": {
                "worker_name": hostname,
                "worker_pid": pid,
                "worker_job_url": url,
                "worker_message": message,
            }
        },
    )

    if response.ok:
        return response.json()
    else:
        if retry > MAX_RETRIES:
            response.raise_for_status()
        # sleep for as many seconds as we have retried so that we do not flood the server
        time.sleep(retry)
        return fail_sample_pipeline_step(id, hostname, pid, url, message, retry + 1)


def patch_subjects(subject_id, dob=None, label=None, sex=None, snpsex=None, srysex=None, tags=None):
    uri = server + Url.SUBJECTS.format(id=subject_id)

    payload = dict(dob=dob, label=label, sex=sex, snpsex=snpsex, srysex=srysex, tags=tags)

    # Filter out None values
    payload = dict((k, v) for k, v in payload.items() if v)

    response = requests.patch(uri, json=payload, auth=(user, password))
    response.raise_for_status()

    return response


def import_sample_to_csa(sample_data):
    uri = server + Url.SAMPLE_DATA_SETS
    json_data = dict(sample_data_set=sample_data)
    log.info("Calling '%s' to import sample '%s'", uri, json_data)
    response = requests.post(uri, auth=(user, password), json=json_data)
    log.info("Import sample returned content '%s'", response.content)
    return response


def fetch_sample_data_set(id, retry=0):
    uri = server + Url.SAMPLE_DATA_SET.format(id=id)
    log.info("Calling '%s' to fetch sample_data_set", uri)
    response = requests.get(uri, auth=(user, password))

    if response.ok:
        return response.json()
    else:
        if retry > MAX_RETRIES:
            response.raise_for_status()

        time.sleep(retry)
        fetch_sample_data_set(id, retry + 1)


def get_projects_flagged_for_auto_import():
    uri = server + Url.PROJECTS_SCOPE.format(scope="auto_import")
    log.info("Calling '%s' to fetch list of projects that are flagged for auto import", uri)
    response = requests.get(uri, auth=(user, password))
    log.info("Project scope auto_import returned content '%s'", response.content)
    if response.ok:
        return response.json()
    else:
        response.raise_for_status()


def get_project(project_name):
    uri = server + Url.PROJECT_RETRIEVAL.format(project_name=project_name)
    response = requests.get(uri, auth=(user, password))
    if response.ok:
        return response.json()
    else:
        response.raise_for_status()


def get_credentials(project_key='', service='', lookup_key=''):

    # because of CSA-1538 bug
    lookup_key = lookup_key.lower()
    query_dict = dict()
    # This is mostly  to keep things backwards compatible
    if project_key:
        query_dict['project_key'] = project_key
    if service:
        query_dict['service'] = service
    if lookup_key:
        query_dict['lookup_key'] = lookup_key
    uri = server.rstrip('api') + 'auth/v1' + Auth.build_filter_string(**query_dict)
    return _get(uri)


def get_credentials_for_id(id):
    uri = '%sauth/v1/credentials/%s.json' % (server.rstrip('api'), id)
    return _get(uri)


def add_credentials(owner_key, service, lookup_key, credential_attributes):
    # because of CSA-1538 bug
    lookup_key = lookup_key.lower()

    uri = server.rstrip('api') + 'auth/v1' + Auth.ADD_CREDENTIALS
    log.info("Calling '%s' to add '%s' credentials to CSA project '%s'", uri, service, owner_key)
    response = requests.post(
        uri,
        auth=(user, password),
        json={
            "credential": {
                "owner_type": "Project",
                "owner_key": owner_key,
                "service": service,
                "lookup_key": lookup_key,
                "expires": "",
                "credential_attributes": credential_attributes,
            }
        },
    )
    response.raise_for_status()

    try:
        return response.json()
    except Exception:
        log.exception("could not parse JSON response from server while reserving pipeline step")
        raise


def add_s3_credentials(owner_key, lookup_key, aws_key, aws_secret):
    return add_credentials(owner_key, "s3", lookup_key, {"key": aws_key, "secret": aws_secret})


def get_reference_data(version):
    uri = server + Url.REFERENCE_DATA_VERSION.format(id=version)
    log.info("Calling '%s' to fetch reference_data_version", uri)
    response = requests.get(uri, auth=(user, password))

    if response.status_code == requests.codes.not_found:
        return None
    elif response.ok:
        return response.json()


def get_sample_by_org_extid(org_key, extid):
    uri = server + Url.SAMPLE_ORG_EXTID.format(org_key=org_key, extid=extid)
    response = requests.get(uri, auth=(user, password))
    if response.ok:
        return response.json()
    else:
        return None


def add_reference_data(ref_data):
    uri = server + Url.REFERENCE_DATA_VERSIONS
    # CSA Api does not care about patches, so they roll it into the minor version
    minor = '-'.join([ref_data.minor, ref_data.patch])
    vep_path = 'vep_v' + ref_data.ensembl
    data = dict(
        base_path=ref_data.path,
        build=ref_data.build,
        major=ref_data.ensembl,
        minor=minor,
        vep_path=vep_path,
    )
    json_data = dict(reference_data_version=data)
    log.info("Calling '%s' to import reference data version '%s'", uri, json_data)
    response = requests.post(uri, auth=(user, password), json=json_data)
    log.info("Register reference data returned content '%s'", response.content)
    return response
