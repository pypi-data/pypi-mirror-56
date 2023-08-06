import os
import uuid
import string
import random

import aiofiles
import aiohttp

from aioify import aioify
from python_settings import settings


class FileWorker(object):
    def __init__(self, path: str = settings.DATA_PATH):
        self._path = path
        
    async def _get_file_path(self, filename, subdir):
        _, file_extension = os.path.splitext(filename)
        generated_file_name = str(uuid.uuid4())
        dir_path = os.path.join(
            self._path,
            subdir,
            generated_file_name[0:2],
            generated_file_name[2:4],
        )
        aios = aioify(obj=os, name='aios')
        await aios.makedirs(name=dir_path, exist_ok=True)
        file_path = os.path.join(dir_path, generated_file_name[4:] + '.' + file_extension)
        return file_path
    
    async def write(self,
                    part: aiohttp.BodyPartReader,
                    filename: str,
                    subdir: str = ''):

        file_path = await self._get_file_path(filename, subdir)
        
        async with aiofiles.open(file_path, mode='wb') as f:
            while True:
                chunk = await part.read_chunk()  # 8192 bytes by default.
                if not chunk:
                    break
                await f.write(chunk)
            
        return file_path
    
    async def read_file(self, file_path: str):
        # TODO: Chunks
        async with aiofiles.open(file_path, 'rb') as f:
            return await f.read()

            