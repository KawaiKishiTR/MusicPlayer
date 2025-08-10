from .playlistParserAPI import playlistParserAPI
from .urlCollectionAPI import urlCollectionAPI
from .urlDownloadAPI import urlDownloadAPI
from .musicfileAPI import musicfileAPI
import asyncio
import pathlib
import abc


#TODO: add database system to it


class generalManager(abc.ABC):
    def __init__(self, playlistManager:type[playlistParserAPI],
                 urlCollectionManager:type[urlCollectionAPI],
                 urlDownloadManager:type[urlDownloadAPI],
                 musicfileManager:type[musicfileAPI]):
        self.playlistManager = playlistManager
        self.urlCollecitonManager = urlCollectionManager
        self.urlDownloadManager = urlDownloadManager
        self.musicfileManager = musicfileManager

        
        self.playlistManager._manager = self
        self.urlCollecitonManager._manager = self
        self.urlDownloadManager._manager = self
        self.musicfileManager._manager = self


    def download(self, *urls, collection_slicer = None):
        state = "unknown"
        item = urls

        if len(item) < 2 and "list=" in item[0]:
            item = self.playlistManager(item)
            state = "playlist"
        elif len(urls) > 1:
            item = self.urlCollecitonManager(*item)
            state = "urlcollection"
        else:
            item = self.urlDownloadManager(item)
            state = "single"
        

        if state == "playlist":
            item = item.parse()
            state = "urlcollection"
        if state == "urlcollection":
            if collection_slicer is not None:
                item = item[collection_slicer]
            asyncio.run(item.download())
        elif state == "single":
            asyncio.run(item.download())


    @abc.abstractmethod
    def load(self, path:pathlib.Path):
        pass
