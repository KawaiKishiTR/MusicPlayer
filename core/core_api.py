import data_structure
import concurrent
import pathlib
import files
import uuid
import abc

class playlistParserAPI(abc.ABC):
    def __init__(self, url:str):
        self.url = url
        self._video_urls: urlCollectionAPI = None

    @abc.abstractmethod
    def parse(self) -> "urlCollectionAPI":
        pass

    @property
    def video_urls(self) -> "urlCollectionAPI":
        if self._video_urls is None:
            self._video_urls = self.parse()
        return self._video_urls

    def __getitem__(self, index) -> "urlCollectionAPI":
        return self.video_urls[index]        


class urlCollectionAPI(abc.ABC):
    def __init__(self, *urls:str):
        self.urls = urls

    def __getitem__(self, index) -> "urlCollectionAPI":
        self.__class__.__init__(self.urls[index])

    @abc.abstractmethod
    def download(self):
        pass


class urlDownloadAPI(abc.ABC):
    def __init__(self, url:str):
        self.url = url
        self.uuid = uuid.uuid4()

        self.audiodir = files.tempfolder(False).name
        self.thumbnaildir = files.tempfolder(False).name
        
        self._metadata:None | data_structure.video_metadata = None

    @abc.abstractmethod
    def get_thumbnail(self):
        pass

    @abc.abstractmethod
    def get_audio(self):
        pass

    @abc.abstractmethod
    def get_metadata(self):
        pass

    def get_async_data(self, download_audio:bool = True):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            if download_audio:
                executor.submit(self.get_audio)
            executor.submit(self.get_thumbnail)
            executor.submit(self.metadata)


    def zipfile(self, path:pathlib.Path = files.MUSIC, download_audio:bool = True) -> files.kawaimusicFile:
        self.get_async_data(download_audio)
        
        if self._metadata is None:
            self.metadata
        if len(list(self.thumbnaildir.iterdir())) < 1:
            self.get_thumbnail()
        if len(list(self.audiodir.iterdir())) < 1 and download_audio:
            self.get_audio()
        
        audio = None
        if download_audio:
            audio = list(self.audiodir.iterdir())[0]
        thumbnail = list(self.thumbnaildir.iterdir())[0]

        return files.kawaimusicFile.compiler(self.metadata, thumbnail, audio, path)
        
    @property
    def metadata(self):
        if self._metadata is not None:
            return self._metadata
        else:
            return self.get_metadata()


