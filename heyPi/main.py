import speech_recognition as sr
import recognize as rec
from execute import Capture, execute
from voice import say
from time import gmtime, strftime
from respond import get_ip
from respond import internet_on
from colorama import init as colorama_init
from termcolor import colored
from playsound import playsound

trigger = "hey"  # catchphrase
testing = 0  # additional command prints

# Listening to the audio source, the microphone most likely.
# The while loop provides an always-on functionality. Use it if you have to.
# The recognizer instance listens to the microphone and records the audio, which is then sent to one
# of the API


def listen_from_source():

    while True:
        recognizer = sr.Recognizer()
        mic = sr.Microphone()
    # Waiting for catchphrase
        with mic as source:
            # performance hit
            recognizer.adjust_for_ambient_noise(source)
            recognizer.pause_threshold = 0.8
            print_ts(colored("Waiting for catchphrase", 'red'))

            snowboy_config = ('snowboy', 'resources/heypi.pmdl')
            recognizer.listen(source, snowboy_config)

            nested_command()


# Nested Command is the command said by the user after the catchphrase has been accepted
# It has been made into a separate function in case of further development
def nested_command():

    while True:
        try:
            # Trigger recognized, listening to the command
            # say("I'm listening")
            playsound('resources/ding.wav')
            recognizer = sr.Recognizer()
            mic = sr.Microphone()
            with mic as source:
                rec_audio = recognizer.listen(source)
                playsound('resources/dong.wav')
                print_ts_log("Recognizer created the audio file")
                # say("Okay, just a second..")
                next_command = rec.recognize_wit(recognizer, rec_audio)
                print_ts_log("Wit recognized the audio")

                if "stop" in next_command.get_text():
                    playsound('resources/dong.wav')
                    break
                response = execute(next_command)
                print_ts_log("Command was executed")
                say(response)
        except AttributeError:
            say("I'm sorry, try that again")


def print_ts(text):
    time = strftime("%H:%M:%S", gmtime())
    print(colored("[" + time + "] ", 'grey') + text)


def print_ts_log(text):
    if testing is 1:
        time = strftime("%H:%M:%S", gmtime())
        print (colored("[" + time + "] " + text, 'grey'))

def print_config():

    # connected to the internet?
    print(colored('HeyPi 0.1', 'red'))
    print(colored('___________________________________', 'grey'))
    internet = colored('connected', 'green') if internet_on() else colored('disconnected', 'red')
    print("Internet: " + internet)
    if internet_on() is 1:
        ip = get_ip()
        print("IP: " + ip)
        result = rec.test_wit()
        wit_ai = colored('connected', 'green') if isinstance(result, Capture) else colored('disconnected', 'red')
        print("Wit.ai: " + wit_ai)
    else:
        print(colored("Please connect to the Internet.", 'red'))

    print(colored('___________________________________', 'grey'))


# Main function. It contains the instance of speech recognition, which handles microphone settings,
# capturing and transcribing audio.

colorama_init()
print_config()
listen_from_source()

