import abc
import pathlib
import core.Structure as Structure
import asyncio
import typing
import json
import uuid

if typing.TYPE_CHECKING:
    from .generalManagerAPI import generalManager
    
#TODO: download metodundan Playlist çıktısı alınmalı ve veri tabanı etkileşimleri
class urlCollectionAPI(abc.ABC):
    _manager:"generalManager" = None
    semaphore = asyncio.Semaphore(5)

    def __init__(self, *urls:str):
        self.urls = urls
    

    def __getitem__(self, index):
        return self.__class__(self.urls[index])


    async def async_download(self, path:pathlib.Path = Structure.MUSIC, download_audio:bool = True):
        uuids = []
        for url in self.urls:
            async with self.semaphore: 
                YT = self._manager.urlDownloadManager(url)
                await YT.async_download(path, download_audio)
                uuids.append(YT.uuid.hex)
        json.dump(uuids, open(Structure.PLAYLIST / uuid.uuid4().hex, "w", encoding="utf-8"), indent=4)



