from termcolor import colored
from gtts import gTTS
import os
from time import gmtime, strftime


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

