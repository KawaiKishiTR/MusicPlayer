import core.Structure as Structure
import zipfile
import pathlib
import typing
import shutil
import json
import abc

if typing.TYPE_CHECKING:
    from .generalManagerAPI import generalManager

#TODO:compile olduğu zaman veri tabanına eklenmeli
class musicfileCompilerAPI(abc.ABC):
    _suffix = "musicfile"
    _audio_name = "audio"
    _thumbnail_name = "thumbnail"
    def __init__(self, metadata:Structure.video_metadata,  thumbnail_path:pathlib.Path, audio_path:pathlib.Path=None, result_path:pathlib.Path = Structure.MUSIC):
        self.metadata = metadata
        self.thumbnail_path = thumbnail_path
        self.audio_path = audio_path
        self.result_path = result_path
    
    def compile(self):
        with zipfile.ZipFile(self.result_path / (self.metadata.title + f".{self.__class__._suffix}"), "w") as archive:
            if self.audio_path is not None:
                archive.write(self.audio_path, arcname=self.__class__._audio_name)
            archive.write(self.thumbnail_path, arcname=self.__class__._thumbnail_name)
            archive.writestr("metadata.json", json.dumps(self.metadata.get_dict(), indent=4))
            self.archive_path = archive.filename
            
        shutil.rmtree(self.thumbnail_path.parent)
        shutil.rmtree(self.audio_path.parent)
        return self.archive_path

class musicfileAPI(abc.ABC):
    _manager:"generalManager" = None
    _compiler = musicfileCompilerAPI
    
    @classmethod
    def compile(cls, metadata:Structure.video_metadata,  thumbnail_path:pathlib.Path, audio_path:pathlib.Path=None, result_path:pathlib.Path = Structure.MUSIC):
        return cls(cls._compiler(metadata, thumbnail_path, audio_path, result_path).compile())

    def __init__(self, musicfile_path:pathlib.Path):
        self.path = musicfile_path

        self.audio_path:str = None
        self.thumbanil_path:str = None 


    def __del__(self):
        if self.audio_path is not None and (path:=pathlib.Path(self.audio_path)).exists():
            path.unlink()
        if self.thumbanil_path is not None and (path:=pathlib.Path(self.thumbanil_path)).exists():
            path.unlink()

    def _load(self, item_name:str):
        with zipfile.ZipFile(self.path, "r") as zf:
            with zf.open(item_name) as item:
                with Structure.tempfile(False) as tmp:
                    tmp.write(item.read())
                    return tmp.name

    def load_thumbnail(self):
        if self.thumbanil_path is None:
            self.thumbanil_path = self._load(self._compiler._thumbnail_name)
        return self.thumbanil_path
    
    def load_audio(self):
        if self.audio_path is None:
            self.audio_path = self._load(self._compiler._audio_name)
        return self.audio_path



