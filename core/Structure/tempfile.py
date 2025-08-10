from .folders import TEMP
import pathlib
import uuid

class tempfile:
    def __init__(self, delete:bool=True, suffix:str = ""):
        self.delete = delete
        self.suffix = suffix
        self.name:pathlib.Path = None
        self.f = None
        self.open()
    
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