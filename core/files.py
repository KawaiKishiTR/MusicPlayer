
import data_structure
import zipfile
import pathlib
import shutil
import uuid
import json


FOLDER = pathlib.Path(__file__).parent.parent
CORE = FOLDER / "core"
DATA = FOLDER / "data"
TEMP = FOLDER / "temp"
MUSIC = FOLDER / "music"
PLAYLIST = FOLDER / "playlists"


class tempfolder:
    def __init__(self, delete:bool=True):
        self.delete = delete
        self.name:pathlib.Path = None
    
    def open(self):
        if self.name is not None:
            return self.name

        self.name = TEMP / uuid.uuid4().hex
        self.name.mkdir()
        return self.name

    def __enter__(self):
        self.open()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.name is None:
            return True
        
        if self.delete:
            shutil.rmtree(self.name)
            self.name = None

        return True


class tempfile:
    def __init__(self, delete:bool=True, suffix:str = ""):
        self.delete = delete
        self.suffix = suffix
        self.name:pathlib.Path = None
        self.f = None
    
    def open(self):
        if self.name is not None:
            return self.name

        self.name = TEMP / (uuid.uuid4().hex + self.suffix)
        self.name.touch()
        self.f = open(self.name, "wb")
        return self.name
    
    def close(self):
        if self.name is None:
            return True
        
        self.f.close()
        self.name.unlink()
        self.name = None

        return True

    def write(self, buffer:bytearray | bytes):
        if (self.f is not None) and (not self.f.closed):
            return self.f.write(buffer)
        return 0

    def __enter__(self):
        self.open()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.name is None:
            return True
        
        if self.delete:
            self.close()

        return True

#TODO:compile olduğu zaman veri tabanına eklenmeli
class kawaimusicFileCompiler:
    def __init__(self, metadata:data_structure.video_metadata,  thumbnail_path:pathlib.Path, audio_path:pathlib.Path=None, result_path:pathlib.Path = MUSIC):
        self.metadata = metadata
        self.thumbnail_path = thumbnail_path
        self.audio_path = audio_path
        self.result_path = result_path
    
    def compile(self):
        with zipfile.ZipFile(self.result_path / (self.metadata.title + ".kawaimusic"), "w") as archive:
            if self.audio_path is not None:
                archive.write(self.audio_path, arcname="audio")
            archive.write(self.thumbnail_path, arcname="thumbnail")
            archive.writestr("metadata.json", json.dumps(self.metadata.get_dict(), indent=4))
            print(archive.filename)
            self.archive_path = archive.filename
            
        shutil.rmtree(self.thumbnaildir)
        shutil.rmtree(self.audiodir)
        

class kawaimusicFile:
    @classmethod
    def compiler(cls, metadata:data_structure.video_metadata,  thumbnail_path:pathlib.Path, audio_path:pathlib.Path=None, result_path:pathlib.Path = MUSIC):
        return kawaimusicFileCompiler(metadata, thumbnail_path, audio_path, result_path)

    def __init__(self, kawaimusicfile_path:pathlib.Path):
        self.path = kawaimusicfile_path
    
    #TODO: dosyayı okuma ve içeriğe erişme protokollerini yaz
    
        
