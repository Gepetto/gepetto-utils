#!/usr/bin/env python

import argparse
import datetime
import logging
import re

args = argparse.ArgumentParser()
args.add_argument('filename', type=argparse.FileType('r'))
args.add_argument('-v', '--verbose', action='store_true')

logging.basicConfig()
logger = logging.getLogger('parse_muscod_logs')


def parse_muscod_logs(filename, verbose):
    """
    Parse muscod's logs to get NDIS, the number of iterations & total computation time
    """

    ndis = iterations = total = None
    logger.setLevel(logging.INFO if verbose else logging.WARNING)

    for number, line in enumerate(filename):
        if 'NDIS' in line:
            ndis = int(line.split('=')[1].strip())
            logger.info('found NDIS on line %i: %s' % (number, ndis))
        elif '**** SQP iteration' in line:  # Only the last will be remembered
            iterations = int(line.split(' ')[3].strip())
            logger.info('found iterations on line %i: %s' % (number, iterations))
        elif '  Total' in line:  # double space to avoid 'Grand Total' line
            total_dict = re.search('(?P<minutes>\d{2}):(?P<seconds>\d{2}).(?P<milliseconds>\d{3})', line).groupdict()
            total = datetime.timedelta(**{k: int(v) for k, v in total_dict.items()})
            logger.info('found total on line %i: %s' % (number, total))

    if ndis is None:
        logger.error('NDIS not found')
    if iterations is None:
        logger.error('iterations not found')
    if total is None:
        logger.error('total not found')

    return {'ndis': ndis, 'iterations': iterations, 'total': total}


if __name__ == '__main__':
    ret = parse_muscod_logs(**vars(args.parse_args()))
    print(ret)
