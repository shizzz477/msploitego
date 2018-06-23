#!/usr/bin/env python

import shlex
import subprocess

__author__ = 'Marc Gurreri'
__copyright__ = 'Copyright 2018, msploitego Project'
__credits__ = []
__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Marc Gurreri'
__email__ = 'marcgurreri@gmail.com'
__status__ = 'Development'

def bashrunner(cmd):
    task = subprocess.Popen(args=shlex.split(cmd),
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 universal_newlines=True,
                                 bufsize=0)

    taskoutput = []
    while task.poll() is None:
        for streamline in iter(task.stdout.readline, ''):
            if isinstance(streamline, unicode):
                streamline = streamline.encode("ascii", "replace")
            taskoutput.append(streamline)
    return taskoutput