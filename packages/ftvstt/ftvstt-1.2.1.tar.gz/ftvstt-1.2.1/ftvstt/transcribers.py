import abc
import ftvstt.exceptions as exceptions


class Transcriber(abc.ABC):
    def __init__(self):
        self.authed = False
        super().__init__()

    @abc.abstractmethod
    def authenticate(self):
        pass

    @exceptions.transcribe_error_handler
    @abc.abstractmethod
    def transcribe(self, inputPath, lang="lang"):
        pass

    @abc.abstractmethod
    def set_text(self, transcript):
        pass

    @abc.abstractmethod
    def set_words(self, transcript):
        pass

    @abc.abstractmethod
    def deauthenticate(self):
        pass
