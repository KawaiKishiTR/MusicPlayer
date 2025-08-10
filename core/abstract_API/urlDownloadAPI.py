import Structure
import asyncio
import pathlib
import typing
import uuid
import abc

if typing.TYPE_CHECKING:
    from .generalManagerAPI import generalManager

class urlDownloadAPI(abc.ABC):
    _manager:"generalManager" = None
    def __init__(self, url:str):
        self.url = url
        self.uuid = uuid.uuid4()

        self.audiodir:pathlib.Path = None
        self.thumbnaildir:pathlib.Path = None
        self.metadata:Structure.video_metadata = None

        self.semaphore = self._manager.urlCollecitonManager.semaphore

    # ------sync methods------
    def get_thumbnail(self):
        if self.thumbnaildir is None:
            self.download_thumbnail()
        return self.thumbnaildir

    def get_audio(self):
        if self.audiodir is None:
            self.download_audio()
        return self.audiodir

    def get_metadata(self):
        if self.metadata is None:
            self.download_metadata()
        return self.metadata

    @abc.abstractmethod
    def download_thumbnail(self):
        pass

    @abc.abstractmethod
    def download_audio(self):
        pass

    @abc.abstractmethod
    def download_metadata(self):
        pass



    #------async fonksiyonlar------
    async def async_download(self, path:pathlib.Path = Structure.MUSIC, download_audio:bool = True):
        loop = asyncio.get_running_loop()
        if download_audio:
            await asyncio.gather(
                loop.run_in_executor(None, self.download_thumbnail),
                loop.run_in_executor(None, self.download_metadata),
                loop.run_in_executor(None, self.download_audio)
            )
        else:
            await asyncio.gather(
                loop.run_in_executor(None, self.download_thumbnail),
                loop.run_in_executor(None, self.download_metadata)
            )
        audio = None
        if download_audio:
            audio = list(self.audiodir.iterdir())[0]
        thumbnail = list(self.thumbnaildir.iterdir())[0]

        return self._manager.musicfileManager.compiler(self.metadata, thumbnail, audio, path)


    async def download(self, path:pathlib.Path = Structure.MUSIC, download_audio:bool = True):
        async with self.semaphore:
            await self.async_download(path, download_audio)


        
