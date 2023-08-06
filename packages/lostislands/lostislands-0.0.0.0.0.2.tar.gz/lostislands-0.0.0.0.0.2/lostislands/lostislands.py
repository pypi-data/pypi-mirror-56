import aiohttp
import logging

log = logging.getLogger(__name__)

class LostIslands:

    def __init__(self, **kwargs):
        self.BASE = "https://api.lostislands.hu/v1/"
        self.timeout = 10
    
    def connect(self, token):
        log.info("Connecting to the servers...")
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.BASE}{token}") as resp:
                print(resp.status)
                print(await resp.text())

if __name__ == '__main__':
    main()