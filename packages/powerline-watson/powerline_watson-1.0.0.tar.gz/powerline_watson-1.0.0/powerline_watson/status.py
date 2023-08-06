#!/usr/bin/env python3
# 
# status.py
# Copyright (C) 2019  Miguel de Dios Matias
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import datetime
import json
import re
import subprocess

def status(pl, line='{time}({tags})⏲️', notask="Free", *args, **kwargs):
    """
        Return a segment shows the time tracked in watson. 
        Args:
            pl (object): The powerline logger. 
            commandLine (string): The command line to execute, it can be complex (with pipes).
            line (string): The string to format the content of segment.
                Default value: {time}({tags})⏲️
            PlaceHolders:
                {time}: The time elapsed in the task.
                {start}: The datetime when started the task.
                {tags}: The list of the tags.
                {project}: The project name.
                {human_time}: The time in human format example 'a minute ago'.
                
        Returns:
            segment (list(dict)): The formated line with output of execution command line as powerline segment.
    """
    result = subprocess.run('watson status -p', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if re.match('No project started', result.stdout.decode('utf8')) is not None:
        contents = notask
    else:
        result = subprocess.run('watson status -e', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        human_time = result.stdout.decode('utf8').strip()
        result = subprocess.run('watson log -j -c', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = result.stdout.decode('utf8')
        tasks = json.loads(result)
        for task in tasks:
            if task['id'] == 'current':
                current = task
                break
        project = current['project']
        tags = ','.join([tag for tag in current['tags']])
        start = re.match('([^.]*)([.]|\+).*', current['start']).groups()[0]
        start_datetime = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S')
        stop = re.match('([^.]*)([.]|\+).*', current['stop']).groups()[0]
        stop_datetime = datetime.datetime.strptime(stop, '%Y-%m-%dT%H:%M:%S')
        time = '{}'.format(stop_datetime - start_datetime)
        contents = line.format(time=time, start=start, project=project, tags=tags, human_time=human_time)
    return [{
        'contents': contents,
        'highlight_groups': ['information:regular'],
        'divider_highlight_group': None}]
