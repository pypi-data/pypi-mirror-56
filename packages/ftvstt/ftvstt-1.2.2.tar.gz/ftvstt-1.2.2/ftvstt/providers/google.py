from google.cloud import speech_v1p1beta1 as speech
from google.protobuf.json_format import MessageToJson

import os
import json

import ftvstt.transcripts as transcripts
import ftvstt.exceptions as exceptions
import ftvstt.transcribers as transcribers

class Google(transcribers.Transcriber):
    def __init__(self):
        super().__init__()
        self.vocList = None

    rawType = "json"

    def authenticate_with_file(self, credentialsFilePath):
        self.credentialsFilePath = credentialsFilePath

        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.credentialsFilePath
        self.authed = True
        try:
            self.__client = speech.SpeechClient()
        except:
            self.authed = False

        return self.authed

    def deauthenticate(self):
        os.environ.pop('GOOGLE_APPLICATION_CREDENTIALS')
        self.credentialsFilePath = None
        self.authed = False

    @exceptions.transcribe_error_handler
    def transcribe(self, inputPath, sample_rate_hertz=16000, encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16, enable_word_time_offsets=True, enable_speaker_diarization=True, lang="fr-FR"):

        lang = self._make_language_compatible(lang)
        transcript = transcripts.Transcript()
        transcript.inputPath = inputPath
        transcript.provider = self.__class__
        if self.authed:
            with open(transcript.inputPath, 'rb') as inputFile:
                content = inputFile.read()

            audio = speech.types.RecognitionAudio(content=content)

            config = speech.types.RecognitionConfig(
                encoding=encoding,
                sample_rate_hertz=sample_rate_hertz,
                language_code=lang,
                enable_word_time_offsets=enable_word_time_offsets,
                enable_speaker_diarization=enable_speaker_diarization
                )

            if self.vocList is not None:
                config.speech_contexts.add(phrases=self.vocList)

            transcript.success = True
            try:
                response = self.__client.long_running_recognize(config, audio)
                resultJson = MessageToJson(response.result())
                transcript.raw = bytes(resultJson, 'ascii').decode('unicode-escape')
                self.__class__.set_text(transcript)
                self.__class__.set_words(transcript)
            except Exception as e:
                transcript.success = False
                transcript.exception = exceptions.GoogleError("An error has occured during Google Cloud transciption :\n" + str(e))

        else:
            transcript.exception = exceptions.GoogleAuthError()
            transcript.success = False
        return transcript

    def set_text(transcript):
        data = json.loads(transcript.raw)
        transcript.text = ""
        for result in data['results']:
            if 'transcript' in result['alternatives'][0].keys():
                transcript.text += result['alternatives'][0]['transcript']
        return transcript.text

    def set_words(transcript):
        transcript.words = []
        transcript.speakers = []
        data = json.loads(transcript.raw)

        for word in data['results'][-1]['alternatives'][0]['words']:
            content = word['word']
            startTime = float(word['startTime'][:-1])
            endTime = float(word['endTime'][:-1])
            speaker = transcripts.Speaker(int(word['speakerTag']))

            if not speaker in transcript.speakers:
                transcript.speakers.append(speaker)

            transcript.words.append( transcripts.Word(content, startTime=startTime, endTime=endTime, speaker=speaker) )

    def set_vocabulary_file(self, vocabularyFilePath):
        exception = None
        if self.authed:
            with open(vocabularyFilePath) as vocabularyFile:
                self.vocList = vocabularyFile.read().splitlines()
        else:
            exception = exceptions.GoogleAuthError()

        if exception:
            self.__vocList = None
            raise exception


    def _make_language_compatible(self, lang):
        if lang[2]=='-':
            lang = lang[:2].lower()+lang[2:].upper()
        return lang
