import data_structure
import core_api
import zipfile
import pathlib
import yt_dlp
import yt_api
import files
import uuid
import json
import vlc



class YT_playlistParser(core_api.playlistParserAPI):
    def parse(self) -> "YT_urlCollection":
        with yt_dlp.YoutubeDL(yt_api.YT_PLAYLIST_PARSER_API) as ydl:
            info = ydl.extract_info(self.url, download=False)

            return YT_urlCollection(*[entry["url"] for entry in info["entries"]])

#TODO: download metodundan Playlist çıktısı alınmalı ve veri tabanı etkileşimleri
class YT_urlCollection(core_api.urlCollectionAPI):
    def download(self):
        uuids = {}
        for url in self.urls:
            YT = YT_urlDownload(url)
            YT.export()
            uuids[YT.uuid.hex] = YT.archive_path
        json.dump(uuids, open(files.PLAYLIST / uuid.uuid4().hex, "w", encoding="utf-8"))


class YT_urlDownload(core_api.urlDownloadAPI):
    def get_metadata(self) -> data_structure.video_metadata:
        with yt_dlp.YoutubeDL(yt_api.YT_INFO_API) as ydl:
            info = ydl.extract_info(self.url, download = False)

            metadata = {
                "title": info.get("title"),
                "uploader": info.get("uploader"),
                "upload_date": info.get("upload_date"),
                "track": info.get("track"),
                "artist": info.get("artist"),
                "url": self.url,
                "uuid": self.uuid.hex
            }

            self._metadata = data_structure.video_metadata(**metadata)
            return self._metadata

    def get_thumbnail(self):
        api = yt_api.YT_THUMBNAIL_API.copy()
        api["outtmpl"] = str(self.thumbnaildir / api["outtmpl"])

        with yt_dlp.YoutubeDL(api) as ydl:
            ydl.download([self.url])

    def get_audio(self):
        api = yt_api.YT_AUDIO_API.copy()
        api["outtmpl"] = str(self.audiodir / api["outtmpl"])

        with yt_dlp.YoutubeDL(api) as ydl:
            ydl.download([self.url])

#TODO: bu sınıf yeniden değerlendirilmeli
class kawaimusic:
    def __init__(self, path:pathlib.Path):
        self.path = path

        self.audio_path:str = None
        self.thumbanil_path:str = None
    
    def __del__(self):
        if self.audio_path is not None and (path:=pathlib.Path(self.audio_path)).exists():
            path.unlink()
        if self.thumbanil_path is not None and (path:=pathlib.Path(self.thumbanil_path)).exists():
            path.unlink()

    def load_thumbnail(self):
        if self.thumbanil_path is not None:
            return self.thumbanil_path
        with zipfile.ZipFile(self.path, "r") as zf:
            with zf.open("thumbnail") as thumbnail:
                with files.tempfile(False) as tmp:
                    tmp.write(thumbnail.read())
                    self.thumbanil_path = tmp.name
        return self.thumbanil_path
    
    def load_audio(self):
        if self.audio_path is not None:
            return self.audio_path
        with zipfile.ZipFile(self.path, "r") as zf:
            with zf.open("audio") as audio:
                with files.tempfile(delete=False) as tmp:
                    tmp.write(audio.read())
                    self.audio_path = tmp.name
        return self.audio_path
    
    def load(self):
        return [self.load_thumbnail(),
                self.load_audio()]

    def play(self):
        self.load()

        player = vlc.MediaPlayer(self.audio_path)
        player.play()




