# importing libraries
import speech_recognition as sr
import os
from os import walk
import sys
import shutil
import time
from pydub import AudioSegment
from pydub.silence import split_on_silence
from moviepy.editor import AudioFileClip

START_TIME = time.time()
READ_PATH = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../..', 'EECS2311\\Lecture_Videos'))
WRITE_AUDIO_PATH = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../..', 'EECS2311\\Lecture_Audio'))
WRITE_PATH = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../..', 'EECS2311\\Lecture_Transcripts'))


# create a speech recognition object
r = sr.Recognizer()

# Read all files from folder
def read_files(READ_PATH):
    print("read_files")
    print(READ_PATH)
    filenames = next(walk(READ_PATH), (None, None, []))[2]  # [] if no file

    # Go through each file from folder individually
    for file in filenames:
        filename = READ_PATH+'\\'+file
        sound_filename = WRITE_AUDIO_PATH+'\\'+file.replace(" ", "_").split('.mp4')[0]+'.wav'
        transcript_filename = WRITE_PATH+'\\'+file.replace(" ", "_").split('.mp4')[0]+'.txt'
        print(filename)
        print(sound_filename)
        print(transcript_filename)

        # Checks if the result file exists
        if not os.path.exists(transcript_filename):
            video_to_audio(filename, sound_filename)
            get_large_audio_transcription(sound_filename, transcript_filename)
        else:
            print(transcript_filename+" file exists.")

        # input("Press enter to continue...")

    return 0

def video_to_audio(video_file, audio_file_name):
    audioclip = AudioFileClip(video_file)
    audioclip.write_audiofile(audio_file_name)


# a function that splits the audio file into chunks
# and applies speech recognition
def get_large_audio_transcription(sound_filename, transcript_filename):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    # open the audio file using pydub
    sound = AudioSegment.from_wav(sound_filename)
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                # print("Error:", str(e))
                f = open(transcript_filename, "a")
                f.write("Error:"+str(e))
                f.write("\n")
            else:
                text = f"{text.capitalize()}. "
                # print(chunk_filename, ":", text)
                whole_text += text
                f = open(transcript_filename, "a")
                f.write(text)
                f.write("\n")
    # remove folder with chunks
    try:
        shutil.rmtree(folder_name)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))

    return 1


read_files(READ_PATH)
print("My program took", time.time() - START_TIME, "to run")


# Resources
# https://towardsdatascience.com/transcribing-interview-data-from-video-to-text-with-python-5cdb6689eea1
# https://pythonbasics.org/transcribe-audio/
# https://www.thepythoncode.com/article/using-speech-recognition-to-convert-speech-to-text-python
