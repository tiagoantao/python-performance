import asyncio

async def lazy_printer(delay, message):
    await asyncio.sleep(delay)
    print(message)

asyncio.wait([lazy_printer(1, 'I am lazy'), lazy_printer(0, 'Full Speed')])
#asyncio.run()
