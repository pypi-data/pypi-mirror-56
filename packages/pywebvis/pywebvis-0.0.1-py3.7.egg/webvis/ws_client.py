import trio
from sys import stderr
from trio_websocket import open_websocket_url

def main():
    trio.run(request)

async def request():
    try:
        async with open_websocket_url('wss://echo.websocket.org') as ws:
            print("sending message")
            await ws.send_message('hello world!')
            message = await ws.get_message()
            print('Received message: %s' % message)
    except OSError as ose:
        print('Connection attempt failed: %s' % ose, file=stderr)

if __name__=="__main__":
    main()
