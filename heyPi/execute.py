import speech_recognition as sr
import recognize as rec
import time
from respond import Response
from respond import TimeResponse
from respond import WeatherResponse
from respond import StatusResponse
from time import gmtime, strftime
from colorama import init as colorama_init
from termcolor import colored
from voice import say

testing = 0  # additional command prints


# saves the information about previous commands
class Reference:

    def __init__(self):
        self.data = dict()

    def save_location(self, location):
        if location is not None:
            if testing is 1:
                print_ts("Location was saved: " + location)
            self.data['location'] = location

    def get_location(self):
        return self.data.get('location')


# Executes a 'Command' object. At this time it checks if a command contains a specific
# string. If no entities have been found by wit.ai, the command cannot be processed.


class Capture:
    def __init__(self, text, entities):
        self.text = text
        self.entities = entities  # dict
        self.time_recorded = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

    def get_text(self):
        return self.text

    def get_entities(self):
        return self.entities


def execute(capture):

    print_ts(colored("You: ", 'blue') + capture.get_text())
    entities = capture.get_entities()

    if testing is 1:
        print_ts(str(entities))
        print_ts(str(entities.keys()))

    if len(entities) == 0:
        return "Sorry, I don't know what you mean with " + "'" + capture.get_text() + "'"

    else:
        # fallback to generic response
        response = Response()

        if len(entities) == 1:

            if "time" in entities:
                response = TimeResponse(None)
            elif "weather" in entities:
                response = WeatherResponse(None)
            elif "status" in entities:
                response = StatusResponse()

        elif len(entities) == 2:

            if all(k in entities for k in ("weather", "location")):
                location = entities.get("location")[0].get("value")
                response = WeatherResponse(location)
                ref.save_location(location)

            elif all(k in entities for k in ("time", "location")):
                location = entities.get("location")[0].get("value")
                response = TimeResponse(location)
                ref.save_location(location)

            elif all(k in entities for k in ("weather", "reference")):
                location = ref.get_location()
                if location is not None:
                    response = WeatherResponse(location)
                else:
                    if testing is 1:
                        print_ts("Location unknown")
                    location = None
                    say("Where exactly?")
                    while location is None:
                        location = nested_execute("location")
                    response = WeatherResponse(location)

            elif all(k in entities for k in ("time", "reference")):
                location = ref.get_location()
                if location is not None:
                    response = TimeResponse(location)
                else:
                    if testing is 1:
                        print_ts("Location unknown")
                    location = None
                    say("Where exactly?")
                    while location is None:
                        location = nested_execute("location")
                    response = TimeResponse(location)

        return response.get_text()


def nested_execute(type):

    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as audio_source:
        rec_audio = recognizer.listen(audio_source)
        capture = rec.recognize_wit(recognizer, rec_audio)

        print_ts(colored("You: ", 'blue') + capture.get_text())
        entities = capture.get_entities()

        if testing is 1:
            print_ts(str(entities))
            print_ts(str(entities.keys()))

        if len(entities) > 0:
            if "location" in entities and type:
                location = entities.get("location")[0].get("value")
                return location
        else:
            return None


def print_ts(text):
    time = strftime("%H:%M:%S", gmtime())
    print colored("[" + time + "] ", 'grey') + text


colorama_init()
ref = Reference()