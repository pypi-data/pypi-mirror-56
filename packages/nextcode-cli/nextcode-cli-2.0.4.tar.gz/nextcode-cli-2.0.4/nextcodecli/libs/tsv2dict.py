#!/usr/bin/env python
"""
Convert TSV (with header) to a python dictionary
"""

import sys
import pprint

pretty = pprint.PrettyPrinter(indent=4)
warning_count = 0
warning_max = 20

WARN_MSG = "Mismatched %d columns in line %d, but %s in header"


class TsvDict(dict):
    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

    def get_item(self, key, default):
        value = self.get(key, default)
        if value == '':
            value = default

        return value


def parse(file_name):
    with open(file_name, 'r') as f:
        lines = f.readlines()

    samples = {}

    if len(lines) == 0:
        return samples

    headerline = lines[0]

    # Get an array of all the column names in lowercase to avoid
    # case sensitivity issues
    colnames = headerline.rstrip("\n").lower().split("\t")
    for line_num, line in enumerate(lines[1:]):
        parts = line.rstrip("\n").split("\t")
        dct = TsvDict()
        if len(parts) != len(colnames):
            exit_msg = WARN_MSG % (len(parts), line_num + 2, len(colnames))
            raise ValueError(exit_msg)
        else:
            dct = TsvDict(zip(colnames, parts))
            if dct['#sampleid'] not in samples:
                sample = {
                    'subject_id': dct.get_item('subjectid', None),
                    'gender': dct.get_item('gender', None),
                    'product': dct.get_item('product', None),
                    'product_version': dct.get_item('productversion', None),
                    'study_id': dct.get_item('studyid', None),
                    'study_role': dct.get_item('studyrole', None),
                    'affected': dct.get_item('affected', None),
                    'sample_tags': dct.get_item('sampletags', None),
                    'files': [],
                }
                samples[dct['#sampleid']] = sample

            file = {
                'platform': dct.get_item('platform', None),
                'file_type': dct.get_item('filetype', None),
                'compression': dct.get_item('compression', None),
                'data_type': dct.get_item('datatype', None),
                'read_no': dct.get_item('readno', None),
                'part_no': dct.get_item('partno', None),
                'file_name': dct.get_item('filename', None),
                'path': dct.get_item('path', None),
                'md5': dct.get_item('md5', None),
                'file_tags': dct.get_item('filetags', {}),
            }

            samples[dct['#sampleid']]['files'].append(file)

    return samples


if __name__ == '__main__':
    file_name = sys.argv[1]
    parse(file_name)
