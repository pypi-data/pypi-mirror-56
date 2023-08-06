# -*- coding: utf-8 -*-
# Copyright 2019 ICON Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
from asyncio import StreamReader, StreamWriter
from typing import Optional

from iconcommons import Logger

from .message import MessageType, Request, NoneRequest, NoneResponse
from .message_queue import MessageQueue
from .message_unpacker import MessageUnpacker


_TAG = "RCP"


class IPCServer(object):
    def __init__(self):
        self._loop = None
        self._server = None
        self._queue: Optional['MessageQueue'] = None
        self._unpacker: Optional['MessageUnpacker'] = MessageUnpacker()
        self._tasks = []

    def open(self, loop,  message_queue: 'MessageQueue', path: str):
        assert loop
        assert message_queue
        assert isinstance(path, str)

        self._loop = loop
        self._queue = message_queue

        server = asyncio.start_unix_server(self._on_accepted, path)

        self._server = server

    def start(self):
        if self._server is None:
            return

        self._server = self._loop.run_until_complete(self._server)

    def stop(self):
        for t in self._tasks:
            t.cancel()

        if self._server is None:
            return

        self._server.close()

    def close(self):
        if self._server is not None:
            asyncio.wait_for(self._server.wait_closed(), 5)
            self._server = None

        self._loop = None
        self._queue = None
        self._unpacker = None

    def _on_accepted(self, reader: 'StreamReader', writer: 'StreamWriter'):
        Logger.debug(tag=_TAG, msg=f"on_accepted() start: {reader} {writer}")

        self._tasks.append(asyncio.ensure_future(self._on_send(writer)))
        self._tasks.append(asyncio.ensure_future(self._on_recv(reader)))

        Logger.debug(tag=_TAG, msg="on_accepted() end")

    async def _on_send(self, writer: 'StreamWriter'):
        Logger.debug(tag=_TAG, msg="_on_send() start")

        while True:
            try:
                request: 'Request' = await self._queue.get()
                if request.msg_type == MessageType.NONE:
                    self._queue.put_response(
                        NoneResponse.from_list([request.msg_type, request.msg_id])
                    )

                    self._queue.task_done()
                    break

                data: bytes = request.to_bytes()
                Logger.debug(tag=_TAG, msg=f"on_send(): data({data.hex()}")
                Logger.info(tag=_TAG, msg=f"Sending Data : {request}")
                writer.write(data)
                await writer.drain()

                self._queue.task_done()

            except BaseException as e:
                Logger.error(tag=_TAG, msg=str(e))

        writer.close()

        Logger.debug(tag=_TAG, msg="_on_send() end")

    async def _on_recv(self, reader: 'StreamReader'):
        Logger.debug(tag=_TAG, msg="_on_recv() start")

        while True:
            try:
                data: bytes = await reader.read(1024)
                if not isinstance(data, bytes) or len(data) == 0:
                    break

                Logger.debug(tag=_TAG, msg=f"_on_recv(): data({data.hex()})")

                self._unpacker.feed(data)

                for response in self._unpacker:
                    Logger.info(tag=_TAG, msg=f"Received Data : {response}")
                    self._queue.message_handler(response)

            except BaseException as e:
                Logger.error(tag=_TAG, msg=str(e))

        await self._queue.put(NoneRequest())

        Logger.debug(tag=_TAG, msg="_on_recv() end")
