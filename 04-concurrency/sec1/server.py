import asyncio

async def serve_canvas(reader, writer):
    data = await reader.read()
    print(f'Message is: {data.decode()}')

async def main():
    server = await asyncio.start_server(
        serve_canvas, '127.0.0.1', 1936)
    async with server:
        await server.serve_forever()

asyncio.run(main())
