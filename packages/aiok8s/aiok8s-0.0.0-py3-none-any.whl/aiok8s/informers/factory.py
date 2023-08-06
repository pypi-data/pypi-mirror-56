# Copyright 2017 The Kubernetes Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio

from aiok8s.cache import shared_informer


def new(client, default_resync, *, namespace=None):
    return _SharedInformerFactory(client, default_resync, namespace)


class _SharedInformerFactory:
    def __init__(self, client, default_resync, namespace):
        self._client = client
        self._namespace = namespace
        self._lock = asyncio.Lock()
        self._default_resync = default_resync
        self._custom_resync = {}
        self._informers = {}
        self._started_informers = set()

    async def start(self, stop_event):
        async with self._lock:
            for informer_type, informer in self._informers.items():
                if informer_type not in self._started_informers:
                    asyncio.ensure_future(informer.run(stop_event))
                    self._started_informers.add(informer_type)

    async def wait_for_cache_sync(self, stop_event):
        async with self._lock:
            informers = {
                informer_type: informer
                for informer_type, informer in self._informers.items()
                if informer_type in self._started_informers
            }
        return {
            informer_type: shared_informer.wait_for_cache_sync(
                stop_event, informer.has_synced
            )
            for informer_type, informer in informers.items()
        }

    def for_resource(self, resource):
        pass
