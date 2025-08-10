from .folders import TEMP
import uuid
import pathlib
import shutil

class tempfolder:
    def __init__(self, delete:bool=True):
        self.delete = delete
        self.name:pathlib.Path = None
        self.open()
    
    def open(self):
        if self.name is not None:
            return self.name

        self.name = TEMP / uuid.uuid4().hex
        self.name.mkdir()
        return self.name

    def __enter__(self):
        self.open()
        return self
    
    def __exit__(self, *args):
        if self.name is None:
            return True
        
        if self.delete:
            shutil.rmtree(self.name)
            self.name = None

        return True
