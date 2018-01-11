import speech_recognition as sr
from execute import Capture
from execute import execute
import sys
from gtts import gTTS
import os
from time import gmtime, strftime
from respond import get_ip
from respond import internet_on
from colorama import init as colorama_init
from termcolor import colored



trigger = "hey"  # catchphrase
testing = 1  # additional command prints

# saving the last queries / commands for later use
# We need some kind of dictionary to save entities of the commands.
# log = dict()


# Wit.ai is used for the actual language understanding. Is not only returns transcribed audio, but
# but also the intent or keywords of the command, so-called entities, which can be configured on
# their website.
# e.g. "What time is it"  Entity:time
# e.g. "What time is it in Vienna" Entity:time, location


# TODO need to change the return variables
def recognize_wit(recognizer, audio):
    if audio is not None:
        wit_ai_key = "ETJDE6YJR44VJT2X4OGDYOLQGGVIWE65"
        try:
            api_response = recognizer.recognize_wit(audio, key=wit_ai_key, show_all=True)
            capt = Capture(api_response.get('_text'), api_response.get('entities'))
            return capt

        except sr.UnknownValueError:
            print_ts("Wit.ai could not understand audio")
        except sr.RequestError as e:
            print_ts("Could not request results from Wit.ai service; {0}".format(e))
    else:
        say("Sorry, I didn't catch that")


# As mentioned in feedback I have implemented an offline recognition via Sphinx, for the sole
# purpose to recognize the catchphrase from the audio.

def recognize_sphinx(recognizer, audio):
    if audio is not None:
        try:
            api_response = recognizer.recognize_sphinx(audio, language="en-US")
            capt = Capture(api_response.get('_text'), "")

            return capt

        except sr.UnknownValueError:
            print_ts("Sphinx could not understand audio")
        except sr.RequestError as e:
            print_ts("Sphinx error; {0}".format(e))


# Listening to the audio source, the microphone most likely.
# The while loop provides an always-on functionality. Use it if you have to.
# The recognizer instance listens to the microphone and records the audio, which is then sent to one
# of the API

def listen_from_source(recognizer, audio_source):
    # TODO use background_listening for the commands and the main thread for the catchphrase

    # while True:
    #     try:
    #         print_ts(colored("Waiting for catchphrase", 'red'))
    #
    #         rec_audio = recognizer.listen(audio_source)
    #         print_ts_log("Recognizer created the audio file")
    #
    #         command = recognize_wit(recognizer, rec_audio)
    #         print_ts_log("Wit recognized the audio")
    #
    #         print_ts(colored("You: ", 'blue') + command.get_text())
    #         # After the catchphrase has been recognized, the program awaits a command
    #         if trigger in command.get_text():
                nested_command(recognizer, audio_source)
        #     else:
        #         continue
        # except AttributeError:
        #     say("I'm sorry, try that again")


# Nested Command is the command said by the user after the catchphrase has been accepted
# It has been made into a separate function in case of further development
def nested_command(recognizer, audio_source):

    while True:
        #try:
            # Trigger recognized, listening to the command
            say("I'm listening")

            rec_audio = recognizer.listen(audio_source)
            print_ts_log("Recognizer created the audio file")
            # say("Okay, just a second..")
            next_command = recognize_wit(recognizer, rec_audio)
            print_ts_log("Wit recognized the audio")

            if "stop" in next_command.get_text():
                say("Have a nice day!")
                sys.exit()
            response = execute(next_command)
            print_ts_log("Command was executed")
            say(response)
       # except AttributeError:
        #    say("I'm sorry, try that again")


# Provides voice feedback via Google's Text to Speech API.
# saves the mp3 file into 'resources' dir and plays with mpg123 in cli
def say(text):
    if text is not None:
        try:
            tts = gTTS(text=text, lang="en")
            tts.save("../resources/response.mp3")
            # mpg123 for linux / pi
            os.system("mpg123 -q ../resources/response.mp3")

            print_ts(colored("HeyPi: ", 'red') + text)
        except IOError:
            print_ts(colored("The response.mp3 can't be reached: No such file or directory, check the path", "red"))


def print_ts(text):
    time = strftime("%H:%M:%S", gmtime())
    print colored("[" + time + "] ", 'grey') + text


def print_ts_log(text):
    if testing is 1:
        time = strftime("%H:%M:%S", gmtime())
        print colored("[" + time + "] " + text, 'grey')


def print_config():

    #connected to the internet?
    print(colored('HeyPi 0.1', 'red'))
    print(colored('___________________________________', 'grey'))
    internet = colored('connected', 'green') if internet_on() else colored('disconnected', 'red')
    print("Internet: " + internet)
    if internet_on() is 1:
        ip = get_ip()
        print("IP: " + ip)

        #connected to wit?
        audio_file_path = "../resources/test.flac"
        r = sr.Recognizer()
        with sr.AudioFile(audio_file_path) as source:
            audio_file = r.record(source)
            result = recognize_wit(r, audio_file)

        wit_ai = colored('connected', 'green') if isinstance(result, Capture) else colored('disconnected', 'red')
        print("Wit.ai: " + wit_ai)
    else:
        print(colored("Please connect to the Internet.", 'red'))

    print(colored('___________________________________', 'grey'))



# Main function. It contains the instance of speech recognition, which handles microphone settings,
# capturing and transcribing audio.
def init():
    colorama_init()
    #print_config()
    rec = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        rec.adjust_for_ambient_noise(source)
        rec.pause_threshold = 0.8
        listen_from_source(rec, source)


init()

