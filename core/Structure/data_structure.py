import dataclasses


@dataclasses.dataclass
class video_metadata:
    upload_date:str
    uploader:str
    artist:str
    title:str
    track:str
    uuid:str
    url:str


    def get_dict(self):
        return {
            "uuid":self.uuid,
            "url":self.url,
            "title":self.title,
            "uploader":self.uploader,
            "upload_date":self.upload_date,
            "track":self.track,
            "artist":self.artist
        }

