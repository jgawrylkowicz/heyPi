import speech_recognition as sr
from gtts import gTTS
import os
import time

trigger = "hey"

# saving the last queries / commands for later use
# new_dict = dict()


# recognize the captured audio it via wit.ai (online)
def recognize_wit(recognizer, audio):
    if audio is not None:
        wit_ai_key = "ETJDE6YJR44VJT2X4OGDYOLQGGVIWE65"
        try:
            return recognizer.recognize_wit(audio, key=wit_ai_key)
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
            return recognizer.recognize_sphinx(audio, language="en-US")
        except sr.UnknownValueError:
            print("Sphinx could not understand audio")
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))


def say(text):
    if text is not None:
        tts = gTTS(text=text, lang="en")
        tts.save("response.mp3")
        # mpg321 for linux / pi
        os.system("afplay response.mp3")
        print("HeyPi: " + text)


# listen to voice commands
def listen_from_source(recognizer, audio_source):
    # TODO use background_listening for the commands and the main thread for the catchphrase

    #while 1:
        print("Waiting for catchphrase")

        rec_audio = recognizer.listen(audio_source)
        command = recognize_sphinx(recognizer, rec_audio)
        print("You: " + command)

        if trigger in command:
            # Trigger recognized, listening to the command
            say("I'm listening")

            rec_audio = recognizer.listen(audio_source)
            command = recognize_wit(recognizer, rec_audio)

            print("You: " + command)


def init():
    rec = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        rec.adjust_for_ambient_noise(source)
        rec.pause_threshold = 0.8
        listen_from_source(rec, source)


init()

