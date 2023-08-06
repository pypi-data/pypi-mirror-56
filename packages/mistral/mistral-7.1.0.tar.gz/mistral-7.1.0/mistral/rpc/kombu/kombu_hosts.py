# Copyright (c) 2017 Intel Corporation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import itertools
import random
import six

import oslo_messaging as messaging


class KombuHosts(object):
    def __init__(self, conf):
        transport_url = messaging.TransportURL.parse(conf, conf.transport_url)

        if transport_url.hosts:
            self.virtual_host = transport_url.virtual_host
            self.hosts = transport_url.hosts
        else:
            self.virtual_host = conf.oslo_messaging_rabbit.rabbit_virtual_host
            self.hosts = []

            username = conf.oslo_messaging_rabbit.rabbit_userid
            password = conf.oslo_messaging_rabbit.rabbit_password

            for host in conf.oslo_messaging_rabbit.rabbit_hosts:
                hostname, port = host.split(':')

                self.hosts.append(messaging.TransportHost(
                    hostname,
                    int(port),
                    username,
                    password
                ))

        if len(self.hosts) > 1:
            random.shuffle(self.hosts)

        self._hosts_cycle = itertools.cycle(self.hosts)

    def get_host(self):
        return six.next(self._hosts_cycle)
