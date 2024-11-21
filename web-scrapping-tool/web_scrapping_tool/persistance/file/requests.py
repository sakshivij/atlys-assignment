import asyncio
import json

from ..abstract import IPersistanceOperation


class RequestFilePersistance(IPersistanceOperation):
    def __init__(self):
        self.file_path = "./files/requests.json"

    async def _load_data(self):
        def read_file():
            try:
                with open(self.file_path, 'r') as file:
                    return json.load(file)
            except FileNotFoundError:
                return []
        
        return await asyncio.to_thread(read_file)

    async def _write_data(self, data):
        # Use asyncio to run synchronous file I/O in a thread pool
        def write_file():
            with open(self.file_path, 'w') as file:
                json.dump(data, file)
        
        await asyncio.to_thread(write_file)

    async def save(self, **kwargs):
        data = await self._load_data()
        data.append(kwargs)
        await self._write_data(data)
        return len(data) - 1

    async def update(self, **kwargs):
        data = await self._load_data()
        item_id = kwargs.pop('id')
        for index, item in enumerate(data):
            if item.get('id') == item_id:
                data[index].update(kwargs)
                await self._write_data(data)
                return 1
        return 0

    async def get_by_id(self, **kwargs):
        data = await self._load_data()
        item_id = kwargs['id']
        return next((item for item in data if item.get('id') == item_id), None)

    async def get_all(self, **kwargs):
        return await self._load_data()

    async def delete(self, **kwargs):
        data = await self._load_data()
        item_id = kwargs['id']
        new_data = [item for item in data if item.get('id') != item_id]
        if len(new_data) != len(data):
            await self._write_data(new_data)
            return 1
        return 0
