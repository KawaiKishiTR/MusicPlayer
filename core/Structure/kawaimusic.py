import core.abstract_API.musicfileAPI as API

class kawaimusicCompiler(API.musicfileCompilerAPI):
    _suffix = "kawaimusic"

class kawaimusic(API.musicfileAPI):
    _compiler = kawaimusicCompiler

