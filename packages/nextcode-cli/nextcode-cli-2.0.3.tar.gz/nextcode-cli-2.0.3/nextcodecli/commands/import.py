#!/usr/bin/env python

import click
import yaml
from os import path
import time
import sys

if sys.version_info < (3, 0):
    from Queue import Queue  # pylint: disable=E0401
else:
    from queue import Queue

from threading import Thread

import requests

from nextcodecli.libs import tsv2dict
from nextcodecli.libs import csa_api


existing = 0
registered = 0
errors = 0


def is_remote(path):
    parts = path.split('://')
    return len(parts) > 1


def create_sample_data(sample, sample_id, org_key, project_name, skip_processing_state=False):
    sample_data = {
        'extid': sample_id,
        'sample_data_type': sample.get('product'),
        'sample_data_type_version': sample.get('product_version'),
        'initial_study': {
            'extid': sample.get('study_id'),
            'participant_kind': sample.get('study_role'),
            'affected': sample.get('affected'),
        },
        'subject': {
            'extid': sample.get('subject_id'),
            'gender': sample.get('gender'),
            'organization_key': org_key,
            'initial_project_key': project_name,
        },
        'tags': sample.get('sampletags', {}),
        'sample_data_files': [],
    }

    if not skip_processing_state:
        sample_data['processing_state'] = 'uploaded'
    return sample_data


def create_file_data(file):
    file_path = file['path']
    if is_remote(file_path):
        full_path = file_path
    else:
        full_path = path.abspath(path.expanduser(file_path))

    file_tags = file.get('file_tags', {})
    tags = dict(
        {
            'filetype': file['file_type'],
            'platform': file['platform'],
            'datatype': file['data_type'],
            'read_no': file['read_no'],
            'part_no': file['part_no'],
        },
        **file_tags
    )

    file_data = {
        'file_name': file['file_name'],
        'full_path': full_path,
        'platform': file['platform'],
        'sample_type': file['data_type'],
        'file_type': file['file_type'],
        'read_no': file['read_no'],
        'part_no': file['part_no'],
        'md5': file['md5'],
        'tags': tags,
    }
    return file_data


def process_sample(q, results):
    while True:
        params = q.get()
        sample = params.get('sample', None)
        org_key = params.get('org_key', None)
        sample_id = params.get('sample_id', None)
        project_name = params.get('project_name', None)
        skip_processing_state = params.get('skip_processing_state', False)
        global existing
        global registered
        global errors
        sample_data = create_sample_data(
            sample, sample_id, org_key, project_name, skip_processing_state
        )

        for file in sample.get('files'):
            file_data = create_file_data(file)
            sample_data['sample_data_files'].append(file_data)

        try:
            response = csa_api.import_sample_to_csa(sample_data)
            result = response.json()
            status = result.get('meta', {}).get('status', None)
            if status == 'error':
                message = result['error']['full_message']
                print('%s: %s' % (sample_id, message))
                if message == 'Pn has already been taken':
                    existing += 1
                else:
                    errors += 1
            else:
                print('%s imported successfully to %s' % (sample_id, project_name))
                registered += 1
        except Exception:
            print('Exception when parsing json')
            print(response.content)
            print(response.status_code)

        if 500 <= response.status_code <= 599:
            print(response.status_code)
        results.put(result)
        q.task_done()


@click.command()
@click.argument('manifest_file', nargs=1)
@click.argument('project_name', nargs=1)
@click.option('--skip_processing_state', is_flag=True, default=False)
def cli(manifest_file, project_name, skip_processing_state):
    """Import a TSV manifest into CSA.

       Read a legacy TSV manifest and import its samples into a project.

       Warning: TSV import is intended only as a deprecation aid and does not follow a defined schema.

       Before import, CSA will be quieried for project and study data
       and the sample metadata prepared to match that.

       Arguments:

           MANIFEST_FILE    A TSV manifest file describing samples.
           PROJECT_NAME    The internal name of the target project.

       Example:

           $ nextcode import manifest.tsv my_project

           Note: You must have access to the project.
    """

    file_exists = path.isfile(manifest_file)
    if not file_exists:
        raise SystemExit(
            click.style('COULD NOT OPEN MANIFEST FILE - is the path correct ?', fg='red')
        )

    try:
        csa_api.configure_from_environment()
    except ValueError:
        full_path = path.expanduser('~/.nextcode/csa_authentication')
        try:
            with open(full_path, 'r') as stream:
                data = yaml.safe_load(stream)
                server = data.get('url')
                user = data.get('username')
                password = data.get('password')
                csa_api.configure(server, user, password)
        except IOError:
            raise SystemExit('COULD NOT READ CSA CONFIG')

    try:
        project = csa_api.get_project(project_name)
    except requests.exceptions.HTTPError as hex:
        if hex.response.status_code == 401:
            raise SystemExit("Not authorized - please authenticate.")
        raise SystemExit('INVALID PROJECT NAME')

    org_key = project.get('project').get('organization_key')

    manifest = tsv2dict.parse(manifest_file)

    q = Queue(len(manifest) * 2)
    results = Queue(len(manifest))
    for i in range(0, 10):
        t = Thread(target=process_sample, args=(q, results))
        t.daemon = True
        t.start()

    start_time = int(round(time.time() * 1000))
    for sample_id, sample in manifest.items():
        q.put(
            {
                'sample': sample,
                'org_key': org_key,
                'sample_id': sample_id,
                'project_name': project_name,
                'skip_processing_state': skip_processing_state,
            }
        )

    q.join()

    time_diff = (int(round(time.time() * 1000)) - start_time) / 1000

    print("\n### Results ###")
    print('Execution time: %s' % time_diff)
    print('Samples: %s' % len(manifest))
    print("Registered: %s" % registered)
    print("Existing: %s" % existing)
    print("Errors: %s" % errors)
