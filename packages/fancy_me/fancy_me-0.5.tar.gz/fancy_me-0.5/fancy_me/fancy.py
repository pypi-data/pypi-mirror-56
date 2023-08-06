from threading import Thread

import websockets

import asyncio
from fancy_me import logger
from fancy_me.udp import DataServer
from fancy_me.ws import counter


class Ipo(object):
    def __init__(self, ws_host="0.0.0.0", ws_port=5400, udp_host="0.0.0.0", udp_port=5401):
        self.loop = asyncio.get_event_loop()
        self.ws_host = ws_host
        self.ws_port = ws_port
        self.udp_host = udp_host
        self.udp_port = udp_port

        self.ws_server = websockets.serve(counter, ws_host, ws_port)

        self.udp_server = self.loop.create_server(DataServer, udp_host, udp_port)

    def run(self):
        loop = asyncio.new_event_loop()

        async def run_it():
            transport, protocaol = await loop.create_datagram_endpoint(lambda: DataServer(),
                                                                       local_addr=(self.udp_host, self.udp_port))
            while True:
                await asyncio.sleep(3600)

        loop.run_until_complete(run_it())
        loop.run_forever()

    def start(self):
        self.loop.run_until_complete(self.ws_server)

        p = Thread(target=self.run, daemon=True)
        p.start()
        logger.info("start successful")
        logger.info(f"webscoket: {self.ws_port}")
        logger.info(f"udp      : {self.udp_port}")
        self.loop.run_forever()


if __name__ == '__main__':
    io = Ipo()
    io.start()
