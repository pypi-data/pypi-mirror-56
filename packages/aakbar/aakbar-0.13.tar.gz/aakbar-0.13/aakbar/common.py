# -*- coding: utf-8 -*-
'''Global constants and common helper functions.
'''
# standard library imports
import csv
import locale
import logging
import os
import shutil
import sys
from datetime import datetime
from itertools import chain
from pathlib import Path, PosixPath  # python 3.4 or later
# 3rd-party modules
import click
import yaml
import numpy as np
import pandas as pd
import pyfaidx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
# package imports
from .version import version as VERSION

#
# global constants
#
PROGRAM_NAME = 'aakbar'
AUTHOR = 'Joel Berendzen'
EMAIL = 'joelb@ncgr.org'
COPYRIGHT = """Copyright (C) 2016, GenerisBio, LLC.  All rights reserved.
aakbar was written written under contract to  The National Center for Genome Resources.
"""
PROJECT_HOME = 'https://github.com/ncgr/aakbar'
DOCS_HOME = 'https://aakbar.readthedocs.org/en/stable'

DEFAULT_FILE_LOGLEVEL = logging.DEBUG
DEFAULT_STDERR_LOGLEVEL = logging.INFO
DEFAULT_FIRST_N = 0  # only process this many records
STARTTIME = datetime.now()
CONFIG_FILE_ENVVAR = 'AAKBAR_CONFIG_FILE_PATH'
DEFAULT_K = 10
DEFAULT_SIMPLICITY_CUTOFF = 3
DEFAULT_LETTERFREQ_WINDOW = 10  # characters
#
# global logger object
#
logger = logging.getLogger(PROGRAM_NAME)
#
# set locale so grouping works
#
for localename in ['en_US', 'en_US.utf8', 'English_United_States']:
    try:
        locale.setlocale(locale.LC_ALL, localename)
        break
    except BaseException:
        continue
#
# Class definitions begin here.
#
class SimplicityObject(object):
    '''Define the interfaces needed to make simplicity calculations.

    '''

    def __init__(self, default_cutoff=DEFAULT_SIMPLICITY_CUTOFF):
        self.cutoff = default_cutoff
        self.k = None
        self.label = 'null'
        self.desc = 'no simplicity calculation'
        self.testcases = [('     non-repeated', 'ABCDEFGHIJ'),
                          ('Simple Repeated Letters', ''),
                          ('15 in a row', 'AAAAAAAAAAAAAAA')
                          ]

    def set_cutoff(self, cutoff):
        '''Set the lower bound on simplicity.

        :param cutoff:  Cutoff value, lower results in more sequence masked.
        :return: None
        '''
        if cutoff < 2:
            logger.error('Simplicity cutoff must be >=2.')
            sys.exit(1)
        else:
            self.cutoff = cutoff

    def set_k(self, k):
        '''Set the k value over which rolling scores are summed.

        :param k: Number of characters in window.
        :return:  None.
        '''
        if k < 2:
            logger.error('k must be >=2')
            sys.exit(1)
        else:
            self.k = k

    def mask(self, seq):
        '''Returns the input string.

        :param seq: Input string.
        :return: Masked copy of input string.  Must be the same length.
        '''
        return seq

    def score(self, seq):
        '''Count the number masked (by lower-case) over a window.

        :param seq: String of characters.
        :param window_size: Size of window over which to calculate.
        :return: Integer array of counts.
        '''
        is_lower = pd.Series([int(char.islower()) for char in to_str(seq)])
        return is_lower.rolling(window=self.k).sum()[self.k - 1:].astype(int)


class PersistentConfigurationObject(object):
    '''Defines a persistent configuration object

    Attributes:
        :config_dict: Dictionary of configuration parameters.
        :name: Configuration filename.
        :path: Configuration filepath (absolute).
    '''

    def __init__(self, config_dir=None, name='config.yaml'):
        '''Inits the configuration dictionary

        Reads a configuration file from a subdirectory of the
        current working directory.  If that file isn't found,
        then searches in the system-specific configuration directory.
        If that file isn't found either, creates a new file in the
        directory specified by the location parameter.
        '''
        self.name = name
        self._default_dict = {'version': VERSION,
                              'simplicity_object_label': None,
                              'plot_type': 'pdf',
                              'sets': [],
                              'summary': {'dir': None,
                                          'label': None},
                              }

        self._default_path = Path(
            (click.get_app_dir(PROGRAM_NAME) + '/' + self.name))
        self._cwd_path = Path('.' + '/.' + PROGRAM_NAME + '/' + self.name)
        if config_dir is not None:
            self.path = self._get_path_from_dir(config_dir)
        elif self._cwd_path.is_file():
            self.path = self._cwd_path
        else:
            self.path = self._default_path
        if not self.path.exists():
            self.config_dict = {}
            self.path = None
        else:
            with self.path.open('rt') as f:
                self.config_dict = yaml.safe_load(f)

    def _get_path_from_dir(self, dir):
        return Path(
            str(dir) +
            '/.' +
            PROGRAM_NAME +
            '/' +
            self.name).expanduser()

    def _update_config_dict(self):
        '''Update configuration dictionary if necessary
        :param config_dict: Configuration dictionary.
        :return: Updated configuration dictionary.
        '''
        try:
            if self.config_dict['version'] != VERSION:
                # Do whatever updates necessary, depending on version.
                # For now, nothing needs to be done.
                self.config_dict['version'] = VERSION
        except KeyError:
            logger.warning('Initializing config file "%s"',
                           self.path)
            self.config_dict = self._default_dict

    def write_config_dict(self, config_dict=None, dir=None):
        '''Writes a YAML configuration dictionary
        :param config_dict: Configuration dictionary
        :return: None
        '''
        if dir is None or dir is '':
            if self.path is None:
                self.path = self._default_path
        elif dir is '.':
            self.path = self._cwd_path
        else:
            self.path = self._get_path_from_dir(dir)

        if config_dict == {}:
            self.config_dict = self._default_dict
        elif config_dict is not None and config_dict != self.config_dict:
            self.config_dict = config_dict
            self._update_config_dict()

        if not self.path.parent.exists():
            # create parent directory
            logger.debug('Creating config file directory "%s"',
                         self.path.parent)
            try:
                self.path.parent.mkdir(parents=True)
            except OSError:
                logger.error('Unable to create parent directory "%s".',
                             self.path.parent)
                sys.exit(1)
        if not self.path.parent.is_dir():
            logger.error('Path "%s" exists, but is not a directory.',
                         self.path.parent)
            sys.exit(1)
        if not self.path.exists():
            logger.debug('Creating config file "%s"', self.path)
            try:
                self.path.touch()
            except OSError:
                logger.error('Path "%s" is not writable.', self.path)
                sys.exit(1)
        with self.path.open(mode='wt') as f:
            yaml.dump(self.config_dict, f)


config_obj = PersistentConfigurationObject()


class DataSetValidator(click.ParamType):
    '''Validate that set names are defined.
    '''
    global config_obj
    name = 'set'
    all_count = 0

    def convert(self, setname, param, ctx):
        '''Verify that arguments refers to a valid set.

        :param argset:
        :param param:
        :param ctx:
        :return:
        '''
        if setname == 'all':
            self.all_count += 1
            if self.all_count > 1:
                logger.error(
                    '"all" is allowed at most one time in a set list.')
                sys.exit(1)
            else:
                return tuple(config_obj.config_dict['sets'])
        elif setname not in config_obj.config_dict['sets']:
            logger.error('"%s" is not a recognized set', argset)
            sys.exit(1)
        return setname

    def multiple_or_empty_set(self, setlist):
        '''Handle special cases of empty set list or all.

        :param setlist: Setlist from validator that may be 'all' or empty.
        :return:
        '''
        # flatten any tuples due to expansion of 'all'
        if any([isinstance(setname, tuple) for setname in setlist]):
            return tuple(chain(*setlist))
        elif setlist == []:
            logger.error('Empty setlist, make sure sets are defined.')
            sys.exit(1)
        else:
            return setlist


DATA_SET_VALIDATOR = DataSetValidator()


#
# helper functions called by manyy cli functions
#
def get_user_context_obj():
    '''Returns the user context, containing logging and configuration data.

    :return: User context object (dict)
    '''
    return click.get_current_context().obj


def to_str(seq):
    '''Decode bytestring if necessary.

    :param seq: Input bytestring, string, or other sequence.
    :return: String.
    '''
    if isinstance(seq, bytes):
        value = seq.decode('utf-8')
    elif isinstance(seq, str):
        value = seq
    else:
        value = str(seq)
    return value


def to_bytes(seq):
    '''Encode or convert string if necessary.

    :param seq: Input string, bytestring, or other sequence.
    :return: Bytestring.
    '''
    if isinstance(seq, str):
        value = seq.encode('utf-8')
    elif isinstance(seq, bytes):
        value = seq
    else:
        value = bytes(seq)
    return value
