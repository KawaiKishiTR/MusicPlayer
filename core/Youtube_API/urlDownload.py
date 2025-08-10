import core.abstract_API as API
import core.Structure as Structure
from . import dictionary as yt_api
import yt_dlp


class YT_urlDownload(API.urlDownloadAPI):
    def get_metadata(self) -> Structure.video_metadata:
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

            self._metadata = Structure.video_metadata(**metadata)
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
