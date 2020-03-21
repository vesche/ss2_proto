#!/usr/bin/env python

import asyncio
import threading

from blessed import Terminal
from string import printable
from sanic import Sanic
from sanic.websocket import WebSocketProtocol

app = Sanic()
term = Terminal()
print(term.clear + 'ss2 server proto')


class Tmp:
    letter_a = 'a'
    letter_b = str()

tmp = Tmp()


async def _consumer_handler(ws):
    while True:
        data = await ws.recv()
        with term.location(0, 5):
            print(f'RECV: {data}', end='')


async def _producer_handler(ws):
    if tmp.letter_a != tmp.letter_b:
        await ws.send(tmp.letter_a)
        tmp.letter_b = tmp.letter_a
    # non-blocking, ten times a second
    await asyncio.sleep(.1)


@app.websocket('/test/<sysid>')
async def test(request, ws, sysid):
    while True:
        consumer_task = asyncio.ensure_future(_consumer_handler(ws))
        producer_task = asyncio.ensure_future(_producer_handler(ws))
        done, pending = await asyncio.wait(
            [consumer_task, producer_task],
            return_when=asyncio.FIRST_COMPLETED,
        )
        for task in pending:
            task.cancel()


def doitup():
    while True:
        with term.cbreak():
            user_input = term.inkey()
        if user_input in list(printable):
            tmp.letter_a = user_input
            with term.location(0, 4):
                print(f'SEND: {user_input}', end='')


diu = threading.Thread(target=doitup)
diu.daemon = True
diu.start()

app.run(host='0.0.0.0', port=1337, protocol=WebSocketProtocol)
