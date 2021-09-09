# Copyright 2021 DeepMind Technologies Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Common utilities for data pipeline tools."""
import contextlib
import shutil
import tempfile
import time
import json
import psutil
import GPUtil
from typing import Optional

from absl import logging
timings = {}

@contextlib.contextmanager
def tmpdir_manager(base_dir: Optional[str] = None):
  """Context manager that deletes a temporary directory on exit."""
  tmpdir = tempfile.mkdtemp(dir=base_dir)
  try:
    yield tmpdir
  finally:
    shutil.rmtree(tmpdir, ignore_errors=True)


@contextlib.contextmanager
def timing(msg: str):
  logging.info('Started %s', msg)
  tic = time.time()
  val1 = psutil.cpu_percent(interval=None)
  yield
  toc = time.time()
  timings[msg] = (toc-tic) / 60
  timings["CPU Usage For:" + msg] = psutil.cpu_percent(interval=None)
  logging.info('Finished %s in %.3f minutes', msg, (toc - tic)/60)
  print (timings)


def time_dump(name):
    with open(name+ "featureTimer.json", 'w') as f:
      f.write(json.dumps(timings, indent=4))
