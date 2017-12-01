import speech_recognition as sr
from gtts import gTTS
import os
import time
import datetime

trigger = "hey"
testing = 1

# saving the last queries / commands for later use
# log = dict()


class Response:
    # dict needed for generating answers
    def __init__(self, entities):
        self.entities = entities

    def generate(self):
        response = ""
        # return response as a string
        return response


class Capture:
    def __init__(self, text, entities):
        self.text = text
        self.entities = entities  # dict
        self.time_recorded = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

    def get_text(self):
        return self.text

    def get_entities(self):
        return self.entities


# recognize the captured audio it via wit.ai (online)
def recognize_wit(recognizer, audio):
    if audio is not None:
        wit_ai_key = "ETJDE6YJR44VJT2X4OGDYOLQGGVIWE65"
        try:
            api_response = recognizer.recognize_wit(audio, key=wit_ai_key, show_all=True)
            capt = Capture(api_response.get('_text'), api_response.get('entities'))

            return capt

        except sr.UnknownValueError:
            print("Wit.ai could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Wit.ai service; {0}".format(e))
    else:
        say("Sorry, I didn't catch that")


# recognize the captured audio it via sphinx (offline)
def recognize_sphinx(recognizer, audio):
    if audio is not None:
        try:
            api_response = recognizer.recognize_sphinx(audio, language="en-US")
            capt = Capture(api_response.get('_text'), "")

            return capt

        except sr.UnknownValueError:
            print("Sphinx could not understand audio")
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))


def say(text):
    if text is not None:
        # TODO check if the response exists as a file

        tts = gTTS(text=text, lang="en")
        tts.save("resources/response.mp3")
        # mpg321 for linux / pi
        os.system("mpg321 -q resources/response.mp3")
        print("HeyPi: " + text)


# execute a command Object
def execute(command):

    print("You: " + command.get_text())
    if testing is 1:
        print("Entities: " + str(command.get_entities()))

    entities = command.get_entities()
    if len(entities) == 0:
        return "Sorry, I can't process that"
    else:

        keys = entities.keys()
        # example
        if "time" in keys:
            # generate as response object later?
            now = datetime.datetime.now()
            say("It is now " + str(now.hour) + " " + str(now.minute))


# listen and capture the voice commands
def listen_from_source(recognizer, audio_source):
    # TODO use background_listening for the commands and the main thread for the catchphrase

    #while 1:
        # print("Waiting for catchphrase")
        #
        # rec_audio = recognizer.listen(audio_source)
        # command = recognize_sphinx(recognizer, rec_audio)
        # print("You: " + command)
        #
        # if trigger in command:
            # Trigger recognized, listening to the command
            say("I'm listening")

            rec_audio = recognizer.listen(audio_source)
            command = recognize_wit(recognizer, rec_audio)
            execute(command)


def init():
    rec = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        rec.adjust_for_ambient_noise(source)
        rec.pause_threshold = 0.8
        listen_from_source(rec, source)


init()

