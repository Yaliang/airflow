# -*- coding: utf-8 -*-
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import json

from slackclient import SlackClient

from airflow import configuration
from airflow.exceptions import AirflowException


def post_slack_message(channel, text, username='Airflow',
                       icon_url='https://raw.githubusercontent.com/apache/'
                                'airflow/master/airflow/www/static/pin_100.jpg',
                       attachments=None):
    token = configuration.conf.get('slack', 'TOKEN')
    sc = SlackClient(token)
    kparam = {
        'channel': channel,
        'username': username,
        'text': text,
        'icon_url': icon_url,
        'attachments': json.dumps(attachments),
    }
    rc = sc.api_call('chat.postMessage', **kparam)

    if not rc['ok']:
        msg = "Slack API call failed ({})".format(rc['error'])
        raise AirflowException(msg)
