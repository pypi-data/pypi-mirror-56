import logging
import ravel
import asyncio


async def run_cli(system_bus):
    print("HERE")
    await asyncio.sleep(2)

if __name__ == "__main__":
    print("HERE")
    logging.basicConfig(level=logging.INFO)
    system_bus = ravel.system_bus()
    loop = asyncio.get_event_loop()
    system_bus.attach_asyncio(loop)
    loop.run_until_complete(run_cli(system_bus))
