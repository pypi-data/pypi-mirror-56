def transcribe_error_handler(transcribe):
    def decorated_transcribe(*args,**kwargs):
        transcript = transcribe(*args,**kwargs)

        if transcript.exception:
            raise transcript.exception

        return transcript
    return decorated_transcribe


class VocapiaError(Exception):
    def __init__(self, message):
        super().__init__(message)


class VocapiaAuthError(Exception):
    def __init__(self):
        super().__init__("No valid Vocapia authentication.")


class BertinError(Exception):
    def __init__(self, message):
        super().__init__(message)


class BertinAuthError(Exception):
    def __init__(self):
        super().__init__("No valid Bertin authentication.")


class GoogleError(Exception):
    def __init__(self, message):
        super().__init__(message)


class GoogleAuthError(Exception):
    def __init__(self):
        super().__init__("No valid Google Cloud authentication.")


class AmazonError(Exception):
    def __init__(self, message):
        super().__init__(message)


class AmazonAuthError(Exception):
    def __init__(self):
        super().__init__("No valid Amazon authentication.")

