#!/usr/bin/env python
import asyncio
import logging
from typing import Callable, Dict

import requests
import aiohttp

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

headers = {"Content-Type": "application/json;charset=utf-8"}


class BatchConnector:
    def __init__(self, url: str):
        self._url = url

    async def send(self, payload: Dict, callback: Callable):
        emotion_result = requests.request(url=self._url, headers=headers, json=payload["payload"], method="POST").json()
        asyncio.create_task(callback(task_id=payload["task_id"], response={"batch": emotion_result}))


class MyBatchConnector:
    def __init__(self, url: str):
        # self.url = None
        self._url = url

    async def send(self, payload: Dict, callback: Callable):
        # print("================")
        # print(self._url + "++++send other")
        print(payload['payload'])
        if payload['payload']['dialogs'][0]['utterances'][-1]['hypotheses'][0]['confidence'] == 0 and \
                payload['payload']['dialogs'][0]['utterances'][-1]['hypotheses'][1]['confidence'] == 0:
            condition = True
        else:
            condition = False
        if condition:
            response = requests.request(url=self._url, headers=headers, json=payload["payload"], method="POST").json()

            await callback(
                task_id=payload['task_id'],
                response=response[0]
            )
        else:
            response = ['pass', 0]
            await callback(
                task_id=payload['task_id'],
                response=response
            )
        # asyncio.create_task(callback(task_id=payload["task_id"], response={emotion_result[0]}))


class MyHTTPConnector:
    def __init__(self, session: aiohttp.ClientSession, url: str):
        self.session = session
        self.url = url

    async def send(self, payload: Dict, callback: Callable):
        try:
            conditon = True
            if conditon:
                async with self.session.post(self.url, json=payload['payload']) as resp:
                    resp.raise_for_status()
                    response = await resp.json()
                    print("================")
                    print(self.url + "+++receive")
                    print(response)
                await callback(
                    task_id=payload['task_id'],
                    response=response[0]
                )
            else:
                response = ['test other pass', 0.0]
                callback(
                    task_id=payload['task_id'],
                    response=response
                )
        except Exception as e:
            response = e
            await callback(
                task_id=payload['task_id'],
                response=response
            )
