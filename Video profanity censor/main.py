import wave
import json
import moviepy.editor
from vosk import Model, KaldiRecognizer, SetLogLevel
from pydub import AudioSegment


class Word:
    ''' A class representing a word from the JSON format for vosk speech recognition API '''

    def __init__(self, dict):
        '''
        Parameters:
        dict (dict) dictionary from JSON, containing:
            conf (float): degree of confidence, from 0 to 1
            end (float): end time of the pronouncing the word, in seconds
            start (float): start time of the pronouncing the word, in seconds
            word (str): recognized word
        '''

        self.conf = dict["conf"]
        self.end = dict["end"]
        self.start = dict["start"]
        self.word = dict["word"]

    def to_string(self):
        ''' Returns a string describing this instance '''
        return "{:20} from {:.2f} sec to {:.2f} sec, confidence is {:.2f}%".format(
            self.word, self.start, self.end, self.conf*100)


def media_censor(video_file_path: str, censure_sound_path: str, vosk_model_path: 'D:\\vosk-model-small-ru-0.22', censuring_words: list):
    '''Censure from video chosen words
    
    video_file_path
      A path to your videofile
      
    censure_sound_path
      A path to censuring sound (You should use beep sound)
      
    vosk_model_path
      A path to vosk model that you downloaded to your computer
      
    censuring_words
      A list of words you want to censure
    
    '''
    
    video_filename = video_file_path
    audio_filename = video_filename[:video_filename.rindex('.')] + '.wav'
    audio = AudioSegment.from_file(file=audio_filename)
    censure_sound = AudioSegment.from_file(censure_sound_path)
    model = vosk_model_path
    
    # Save audio from video as separate file in the same directory
    moviepy.editor.VideoFileClip(video_filename).audio.write_audiofile(audio_filename)
    # Resave that audio in mono channel (script works with only mono audio!)
    AudioSegment.from_file(file=audio_filename).set_channels(1).export(audio_filename, format='wav')
    
    # preparation to recognition
    wf = wave.open(audio_filename, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    # get the list of JSON dictionaries
    results = []
    # recognize speech using vosk model
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            part_result = json.loads(rec.Result())
            results.append(part_result)
    part_result = json.loads(rec.FinalResult())
    results.append(part_result)

    # convert list of JSON dictionaries to list of 'Word' objects
    list_of_Words = []
    for sentence in results:
        if len(sentence) == 1:
            # sometimes there are bugs in recognition 
            # and it returns an empty dictionary
            # {'text': ''}
            continue
        for obj in sentence['result']:
            w = Word(obj)  # create custom Word object
            list_of_Words.append(w)  # and add it to list
            for word in censuring_words:
                if word in w.word:
                    audio = audio[:w.start * 1000] + censure_sound[:(w.end - w.start) * 1000] + sound[w.end * 1000:]
                    
    # resave past audiofile but now censored
    audio.export(audio_filename, format='wav')
    wf.close()  # close audiofile
    
    # finally set video a censored audio and render
    audioclip = moviepy.editor.AudioFileClip(audio_filename)
    videoclip = moviepy.editor.VideoFileClip(full_video_filename)
    videoclip.audio = audioclip
    videoclip.write_videofile(video_filename[:video_filename.rindex('.')] + '_censored.mp4')
