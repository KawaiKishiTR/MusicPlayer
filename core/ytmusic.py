from dataclasses import dataclass
from typeguard import typechecked
from mimetypes import guess_type
from zipfile import ZipFile
from hashlib import sha256
from yt_dlp import YoutubeDL
from shutil import rmtree
from uuid import uuid4
from files import *
import json
import os

YT_AUDIO_API = {
    'format': 'bestaudio[ext=opus]/bestaudio/best',
    'postprocessors': [
        {
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'opus',
            'preferredquality': '32',
        },
    ],
    'quiet': True,
    'no_warnings': True,
    'outtmpl': '%(title)s.%(ext)s', # dosya isim şablonu
}

YT_THUMBNAIL_API = {
    'quiet': True,
    'writethumbnail': True,
    'skip_download': True,
    'no_warnings': True,
    'outtmpl': '%(title)s.%(ext)s',
}

YT_INFO_API = {
    'skip_download': True,
    'quiet': True,
    'no_warnings': True,
    'outtmpl': '%(title)s.%(ext)s', # dosya isim şablonu
}

@dataclass
class YT_Video_metadata:
    title:str
    uploader:str
    upload_date:str
    track:str
    artist:str

    def __str__(self):
        return f"{self.title}\n{self.uploader}\n{self.upload_date}\n{self.track}\n{self.artist}"


class YTMusıcDownload:
    def __init__(self, url:str):
        self.url = url
        self.uuid = uuid4()
        self.tempfolder = TEMP / str(self.uuid.hex)
        self.tempfolder.mkdir()
        self._metadata:None | YT_Video_metadata = None
    
    @property
    def metadata(self):
        if self._metadata is not None:
            return self._metadata
        else:
            return self.info

    @property
    def info(self) -> YT_Video_metadata:
        with YoutubeDL(YT_INFO_API) as ydl:
            info = ydl.extract_info(self.url, download = False)

            metadata = {
                "title": info.get("title"),
                "uploader": info.get("uploader"),
                "upload_date": info.get("upload_date"),
                "track": info.get("track"),
                "artist": info.get("artist"),
            }

            self._metadata = YT_Video_metadata(**metadata)
            return self._metadata

    def get_thumbnail(self):
        cwd = os.getcwd()
        os.chdir(TEMP / str(self.uuid.hex))

        with YoutubeDL(YT_THUMBNAIL_API) as ydl:
            ydl.download([self.url])

        os.chdir(cwd)

    def get_audio(self):
        cwd = os.getcwd()
        os.chdir(TEMP / str(self.uuid.hex))

        with YoutubeDL(YT_AUDIO_API) as ydl:
            ydl.download([self.url])

        os.chdir(cwd)
            
class kawaimusic:
    @typechecked
    def __init__(self, video_url:YTMusıcDownload|str, path:Path = MUSIC, download_audio:bool = True):
        if isinstance(video_url, str):
            video_url = YTMusıcDownload(video_url)
        
        self.video_url = video_url
        self.download_audio = download_audio
        self.path = path
    
    def export(self, path:Path = None, download_audio:bool = None):
        if path is None:
            path = self.path
        if download_audio is None:
            download_audio = self.download_audio
        
        if download_audio:
            self.video_url.get_audio()
        self.video_url.get_thumbnail()

        with ZipFile(path / (self.video_url.info.title + ".kawaimusic"), "w") as archive:
            archive.writestr("url", self.video_url.url)
            archive.writestr("uuid", self.video_url.uuid.hex)
            for _type, file in [(guess_type(p)[0],p) for p in self.video_url.tempfolder.iterdir()]:
                
                
                if _type.startswith("audio"):
                    archive.write(file, arcname="audio")


                    sha = sha256()
                    with open(file, "rb") as f:
                        for blok in iter(lambda: f.read(4096), b""):
                            sha.update(blok)
                    archive.writestr("hash", sha.hexdigest())


                elif _type.startswith("image"):
                    archive.write(file, arcname="thumbnail")

        if self.video_url.tempfolder.exists() and self.video_url.tempfolder.is_dir():
            rmtree(self.video_url.tempfolder)
            







url = "https://www.youtube.com/watch?v=kPa7bsKwL-c"  # İndirmek istediğin video linki

km = kawaimusic(url)
km.export()
