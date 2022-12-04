"""
   Copyright 2021 UChicago Argonne, LLC

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import os
from datetime import datetime

from src.utils.config import ConfigArguments
from time import time
# UTC timestamp format with microsecond precision
LOG_TS_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"
from mpi4py import MPI

def get_rank():
    return MPI.COMM_WORLD.rank

def get_size():
    return MPI.COMM_WORLD.size

def timeit(func):
    def wrapper(*args, **kwargs):
        begin = time()
        x = func(*args, **kwargs)
        end = time()
        return x, "%10.10f"%begin, "%10.10f"%end, os.getpid()
    return wrapper

def progress(count, total, status=''):
    """
    Printing a progress bar. Will be in the stdout when debug mode is turned on
    """
    _args = ConfigArguments.get_instance()
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + ">"+'-' * (bar_len - filled_len)
    if get_rank()==0:
        if count == 1:
            print("")
        print("\r{}: [{}] {}% {} of {} ".format(status, bar, percents, count, total), end='')
        if count == total:
            print("")
        os.sys.stdout.flush()

def utcnow(format=LOG_TS_FORMAT):
    return datetime.now().strftime(format)

def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')
