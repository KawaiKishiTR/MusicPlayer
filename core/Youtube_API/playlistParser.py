import core.abstract_API as API
import dictionary as yt_api
import yt_dlp


class YT_playlistParser(API.playlistParserAPI):
    def parse(self):
        with yt_dlp.YoutubeDL(yt_api.YT_PLAYLIST_PARSER_API) as ydl:
            info = ydl.extract_info(self.url, download=False)

            return self._manager.urlCollecitonManager(*[entry["url"] for entry in info["entries"]])
