import requests
import xml.etree.ElementTree as ET

import ftvstt.transcripts as transcripts
import ftvstt.exceptions as exceptions
import ftvstt.transcribers as transcribers

class Vocapia(transcribers.Transcriber):
    rawType = "xml"

    def __init__(self, apiBaseUrl):
        super().__init__()

        self.apiBaseUrl = apiBaseUrl
        self.vocabularyFilePath = None

    def __rawType(self):
        return "xml"

    def authenticate(self, user, password):
        self.user = user
        self.password = password
        self.authed = requests.post(self.apiBaseUrl, auth=(self.user, self.password)).status_code == 400
        return self.authed

    def deauthenticate(self):
        self.user = None
        self.password = None
        self.authed = False


    @exceptions.transcribe_error_handler
    def transcribe(self, inputPath, lang="fr-FR"):
        lang = self._make_language_compatible(lang)
        transcript = transcripts.Transcript()
        transcript.inputPath = inputPath
        transcript.provider = self.__class__

        if self.authed:
            payload =   {
                            'method': 'vrbs_trans',
                            'model': lang
                        }

            with open(inputPath, 'rb') as inputFile:
                if self.vocabularyFilePath is None:
                    rep = requests.post(self.apiBaseUrl , files={'audiofile': inputFile}, auth=(self.user, self.password), data=payload)
                else:
                    with open(self.vocabularyFilePath, 'rb') as vocabularyFile:
                        rep = requests.post(self.apiBaseUrl , files={'audiofile': inputFile, 'vocfile' : vocabularyFile}, auth=(self.user, self.password), data=payload)

            resultXMLroot = ET.fromstring(rep.text)
            transcript.success = resultXMLroot.tag != 'Error'
            if transcript.success:
                transcript.raw = rep.text
                self.__class__.set_text(transcript)
                self.__class__.set_words(transcript)
            else:
                transcript.exception = exceptions.VocapiaError('Vocapia error '+ resultXMLroot.attrib['code'] +' : '+  resultXMLroot.text)
        else:
            transcript.exception = exceptions.VocapiaAuthError()
            transcript.success = False
        return transcript

    def set_text(transcript):
        root = ET.fromstring(transcript.raw)
        WordsTag = root.findall('SegmentList/SpeechSegment/Word')
        Words = [word.text for word in WordsTag]
        transcript.text = ""
        for i in range(len(Words)):
            if Words[i][-2] in ["'", "-"]:
                Words[i] = Words[i][:-1]
            if i+1 < len(Words) and Words[i+1][1] in ["-",".",",","!",":","?"]:
                Words[i] = Words[i][:-1]
            transcript.text += Words[i][1:]
        return transcript.text

    def set_words(transcript):
        root = ET.fromstring(transcript.raw)
        speakers = root.findall('SpeakerList/Speaker')
        transcript.speakers = []
        for speaker in speakers:
            gender = speaker.attrib['spkid'][0]
            speakerId = int(speaker.attrib['spkid'][2:])
            transcript.speakers.append( transcripts.Speaker(speakerId,gender=gender) )

        transcript.words = []
        root = ET.fromstring(transcript.raw)
        SpeechSegments = root.findall('SegmentList/SpeechSegment')

        for speechSegment in SpeechSegments:
            gender = speechSegment.attrib['spkid'][0]
            speakerId = int(speechSegment.attrib['spkid'][2:])

            speaker = transcripts.Speaker(speakerId,gender=gender)

            words = list(speechSegment)
            for word in words:
                startTime = float(word.attrib['stime'])
                endTime = startTime + float(word.attrib['dur'])
                confidence = float(word.attrib['conf'])
                content = word.text
                transcript.words.append( transcripts.Word(content, startTime=startTime, endTime=endTime, speaker=speaker, confidence=confidence) )
        return transcript.words

    def set_vocabulary_file(self,vocabularyFilePath):
        if self.authed:
            self.vocabularyFilePath = vocabularyFilePath
        else:
            raise exceptions.VocapiaAuthError()

    def _make_language_compatible(self, lang):
        if lang.upper() in ["FR-FR","FRE","FR"]:
            return "fre"
        elif lang.upper() in ["EN-US", "EN-EN", "ENG", "EN"]:
            return "eng"
        else:
            return lang

