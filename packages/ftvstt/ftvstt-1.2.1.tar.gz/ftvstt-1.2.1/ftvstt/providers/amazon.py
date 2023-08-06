import boto3
import requests

import time
import os
import json

import random as rd

import ftvstt.transcripts as transcripts
import ftvstt.exceptions as exceptions
import ftvstt.transcribers as transcribers

class Amazon(transcribers.Transcriber):
    rawType = "json"
    def __init__(self, bucketName, region_name='eu-west-3'):
        super().__init__()
        self.bucketName = bucketName
        self.region_name = region_name
        self.__vocList = None
        self.__vocName = None

    def authenticate_with_file(self, credentialsFilePath):
        self.credentialsFilePath = credentialsFilePath

        auth = {}
        self.authed = True
        try:
            with open(self.credentialsFilePath, mode="r") as csvFile:
                reader = csv.reader(csvFile, delimiter="=")
                for line in reader:
                    auth[line[0]] = line[1]

            self.__s3Client = boto3.client('s3', aws_access_key_id=auth['AWSAccessKeyId'], aws_secret_access_key=auth['AWSSecretKey'])
            self.__transcribeClient = boto3.client('transcribe', region_name=self.region_name, aws_access_key_id=auth['AWSAccessKeyId'], aws_secret_access_key=auth['AWSSecretKey'])
            client.list_buckets()

        except:
            authed = False

        return self.authed


    def authenticate(self, awsAccessKeyId, awsSecretAccessKey):
        self.id = awsAccessKeyId
        self.password = awsSecretAccessKey

        self.authed = True
        try:
            self.__s3Client = boto3.client('s3', aws_access_key_id=self.id, aws_secret_access_key=self.password)
            self.__transcribeClient = boto3.client('transcribe', region_name=self.region_name, aws_access_key_id=self.id, aws_secret_access_key=self.password)
            client.list_buckets()
        except:
            authed = False

        return self.authed

    def deauthenticate(self):
        self.credentialsFilePath = None
        self.id = None
        self.password = None

        self.__s3Client = None
        self.__transcribeClient = None


    @exceptions.transcribe_error_handler
    def transcribe(self, inputPath, lang="fr-FR", s3file=False): #set s3file=True if the input file is already on S3, in that case inputPath should be the url of the file
        lang = self._make_language_compatible(lang)
        transcript = transcripts.Transcript()
        transcript.inputPath = inputPath
        transcript.provider = self.__class__

        if self.authed:
            if s3file:
                audioUri, transcript.exception = inputPath, None
            else:
                s3AudioPath = "ftvstt/"+os.path.basename(transcript.inputPath)
                audioUri, transcript.exception = self.__s3_upload(transcript.inputPath, s3AudioPath)

            if transcript.exception:
                transcript.success = False
                return transcript

            jobName = "ftvstt_job_"+ str(rd.randint(1,1e6)) +"_"+ os.path.basename(transcript.inputPath).replace(".","_")

            try:
                if self.__vocList is None:
                    self.__transcribeClient.start_transcription_job(
                        TranscriptionJobName=jobName,
                        Media={'MediaFileUri': audioUri},
                        MediaFormat='wav',
                        LanguageCode=lang,
                        Settings={ 'MaxSpeakerLabels' : 10, 'ShowSpeakerLabels' : True}
                    )
                else:
                    self.__transcribeClient.start_transcription_job(
                        TranscriptionJobName=jobName,
                        Media={'MediaFileUri': audioUri},
                        MediaFormat='wav',
                        LanguageCode=lang,
                        Settings={ 'MaxSpeakerLabels' : 10, 'ShowSpeakerLabels' : True, 'VocabularyName': self.__vocName}
                    )
            except Exception as e:
                transcript.exception = exceptions.AmazonError("Amazon Transcription failed : \n" +str(e))
                transcript.success = False
                return transcript


            while True:
                status = self.__transcribeClient.get_transcription_job(TranscriptionJobName=jobName)
                if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
                    break
                time.sleep(1)

            if status['TranscriptionJob']['TranscriptionJobStatus'] == 'FAILED':
                transcript.success = False
                transcript.exception = exceptions.AmazonError("Amazon Transcription failed : \n" + status['TranscriptionJob']['FailureReason'])
            else:
                rawResultsUri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
                rep = requests.get(rawResultsUri)

                transcript.success = rep.status_code != 404

                if not transcript.success:
                    transcript.exception = exceptions.AmazonError("Amazon Transcription failed : \n" + "Impossible to reach transcription result at :" + rawResultsUri)
                    return transcript

            transcript.raw = rep.text
            self.__class__.set_text(transcript)
            self.__class__.set_words(transcript)

            time.sleep(2)
            self.__transcribeClient.delete_transcription_job(TranscriptionJobName=jobName)
        else:
            transcript.exception = exceptions.AmazonAuthError()
            transcript.success = False
        return transcript


    def set_text(transcript):
        data = json.loads(transcript.raw)
        transcript.text = ""
        for result in data['results']['transcripts']:
            transcript.text += result['transcript']
        return transcript.text

    def set_words(transcript):
        transcript.words = []
        transcript.speakers = []

        data = json.loads(transcript.raw)

        segments = data['results']['speaker_labels']['segments']

        for segment in segments:
            if not transcripts.Speaker(int(segment['speaker_label'][4:])) in transcript.speakers:
                transcript.speakers.append( transcripts.Speaker(int(segment['speaker_label'][4:])) )

        for word in data['results']['items']:
            try:
                content = word['alternatives'][0]['content']
                startTime = float(word['start_time'])
                endTime = float(word['end_time'])
                confidence = float(word['alternatives'][0]['confidence'])

                speaker = None

                for segment in segments:
                    if startTime >= float(segment['start_time']) and endTime <= float(segment['end_time']):
                        speaker = transcripts.Speaker(int(segment['speaker_label'][4:]))
                        break

                transcript.words.append( transcripts.Word(content,startTime=startTime,endTime=endTime,confidence=confidence,speaker=speaker) )
            except:
                pass


            transcript.words.append( transcripts.Word(content, startTime=startTime, endTime=endTime, confidence=confidence) )

    def __s3_upload(self, inputPath, s3Path):
        exception = None
        fileUri = None
        try:
            self.__s3Client.upload_file(inputPath, self.bucketName, s3Path)
            fileUri = "https://"+ self.bucketName +".s3."+ self.region_name +".amazonaws.com/" + s3Path
        except Exception as e:
            exception = exceptions.AmazonError("Media upload to Amazon failed : \n" +str(e))
        return fileUri, exception


    def set_vocabulary_file(self, vocabularyFilePath, lang="fr-FR"):
        exception = None
        if self.authed:
            with open(vocabularyFilePath) as vocabularyFile:
                self.__vocList = vocabularyFile.read().splitlines()
            self.__vocName = "ftvstt_voc_"+ str(rd.randint(1,1e6)) +"_"+ os.path.basename(vocabularyFilePath).replace(".","_")
            exception = self.__create_vocabulary_file(lang)
        else:
            exception = exceptions.AmazonAuthError()

        if exception:
            self.__vocList = None
            raise exception


    def __create_vocabulary_file(self, lang):
        exception = None
        self.__transcribeClient.create_vocabulary(
                VocabularyName=self.__vocName,
                LanguageCode=lang,
                Phrases=self.__vocList
            )
        while True:
            status = self.__transcribeClient.get_vocabulary(VocabularyName=self.__vocName)
            if status['VocabularyState'] in ['READY', 'FAILED']:
                break
            time.sleep(1)

        if status['VocabularyState'] == 'FAILED':
            exception = exceptions.AmazonError("Couldn't upload vocabulary file : \n" + status['FailureReason'])
        return exception

    def _make_language_compatible(self, lang):
        if lang[2]=='-':
            lang = lang[:2].lower()+lang[2:].upper()
        return lang
