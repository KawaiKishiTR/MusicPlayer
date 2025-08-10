from .urlCollectionAPI import urlCollectionAPI
import abc
import typing

if typing.TYPE_CHECKING:
    from .generalManagerAPI import generalManager


class playlistParserAPI(abc.ABC):
    _manager:generalManager = None
    def __init__(self, url:str):
        self.url = url
        self._video_urls: urlCollectionAPI = None
    

    @abc.abstractmethod
    def parse(self) -> urlCollectionAPI:
        pass

    @property
    def video_urls(self) -> urlCollectionAPI:
        if self._video_urls is None:
            self._video_urls = self.parse()
        return self._video_urls

    def __getitem__(self, index) -> urlCollectionAPI:
        return self.video_urls[index]        
