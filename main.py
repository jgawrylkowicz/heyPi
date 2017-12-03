import speech_recognition as sr
from gtts import gTTS
import os
import generate as gen

trigger = "hey"  # catchphrase
testing = 1  # additional command prints

# saving the last queries / commands for later use
# We need some kind of dictionary to save entities of the commands.
# log = dict()


# Wit.ai is used for the actual language understanding. Is not only returns transcribed audio, but
# but also the intent or keywords of the command, so-called entities, which can be configured on
# their website.
# e.g. "What time is it"  Entity:time
# e.g. "What time is it in Vienna"  Entity:time, location

def recognize_wit(recognizer, audio):
    if audio is not None:
        wit_ai_key = "ETJDE6YJR44VJT2X4OGDYOLQGGVIWE65"
        try:
            api_response = recognizer.recognize_wit(audio, key=wit_ai_key, show_all=True)
            capt = gen.Capture(api_response.get('_text'), api_response.get('entities'))

            return capt

        except sr.UnknownValueError:
            print("Wit.ai could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Wit.ai service; {0}".format(e))
    else:
        say("Sorry, I didn't catch that")


# As mentioned in feedback I have implemented an offline recognition via Sphinx, for the sole
# purpose to recognize the catchphrase from the audio.

def recognize_sphinx(recognizer, audio):
    if audio is not None:
        try:
            api_response = recognizer.recognize_sphinx(audio, language="en-US")
            capt = gen.Capture(api_response.get('_text'), "")

            return capt

        except sr.UnknownValueError:
            print("Sphinx could not understand audio")
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))


# Provides voice feedback via Google's Text to Speech API.
# saves the mp3 file into 'resources' dir and plays with mpg123 in cli
def say(text):
    if text is not None:
        # TODO check if the response exists as a file

        tts = gTTS(text=text, lang="en")
        tts.save("resources/response.mp3")
        # mpg123 for linux / pi
        os.system("mpg123 -q resources/response.mp3")
        print("HeyPi: " + text)


# Executes a 'Command' object. At this time it checks if a command contains a specific
# string. If no entities have been found by wit.ai, the command cannot be processed.

def execute(command):

    print("You: " + command.get_text())
    if testing is 1:
        print("Entities: " + str(command.get_entities()))

    entities = command.get_entities()
    if len(entities) == 0:
        say("Sorry, I don't know what you mean with '" + command.get_text() + "'")
    else:

        keys = entities.keys()
        # example
        if "time" in keys:
            response = gen.TimeResponse(None)
            say(response.get_text())


# Listening to the audio source, the microphone most likely.
# The while loop provides an always-on functionality. Use it if you have to.
# The recognizer instance listens to the microphone and records the audio, which is then sent to one
# of the API

def listen_from_source(recognizer, audio_source):
    # TODO use background_listening for the commands and the main thread for the catchphrase

    #while 1:
        # print("Waiting for catchphrase")
        #
        # rec_audio = recognizer.listen(audio_source)
        # command = recognize_sphinx(recognizer, rec_audio)
        # print("You: " + command)

        # After the catchphrase has been recognized, the program awaits a command

        # if trigger in command:
            # Trigger recognized, listening to the command
            say("I'm listening")

            rec_audio = recognizer.listen(audio_source)
            command = recognize_wit(recognizer, rec_audio)
            execute(command)


# Main function. It contains the instance of speech recognition, which handles microphone settings,
# capturing and transcribing audio.
def init():
    rec = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        rec.adjust_for_ambient_noise(source)
        rec.pause_threshold = 0.8
        listen_from_source(rec, source)


init()

