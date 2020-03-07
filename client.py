import uuid
import websocket
import _thread as thread

from blessed import Terminal
from string import printable

sysid = str(uuid.uuid1(uuid.getnode(),0))[24:]
term = Terminal()
print(term.clear + 'ss2 client proto')


class Client:
    def __init__(self):
        self.ws = websocket.WebSocketApp(
            f'ws://127.0.0.1:1337/test/{sysid}',
            on_message=self.on_message
        )
        self.ws.on_open = self.on_open

    @staticmethod
    def on_message(ws, message):
        with term.location(0, 5):
            print(f'RECV: {message}', end='')

    @staticmethod
    def on_open(ws):
        thread.start_new_thread(doitup, (ws,))


def doitup(ws):
    while True:
        with term.cbreak():
            user_input = term.inkey()
        if repr(user_input) == 'KEY_ESCAPE':
            break
        if user_input in list(printable):
            ws.send(user_input)
            with term.location(0, 4):
                print(f'SEND: {user_input}', end='')
    ws.close()


c = Client()
c.ws.run_forever()
