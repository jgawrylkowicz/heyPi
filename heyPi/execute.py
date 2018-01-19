import speech_recognition as sr
import recognize as rec
import time
import datetime
from respond import Response
from respond import TimeResponse
from respond import WeatherResponse
from respond import StatusResponse
from respond import ConnectionResponse
from respond import NoteResponse
from time import gmtime, strftime
from colorama import init as colorama_init
from termcolor import colored
from voice import say
from playsound import playsound

testing = 0  # additional command prints


# saves the information about previous commands
class Memory:

    def __init__(self):
        self.data = dict()
        # save the dict locally

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


def filter_by_confidence(entities):
    if entities is not None:
        for key, values in entities.items():
            if values[0].get("confidence") <= 0.8:
                entities.pop(key, None)


def execute(capture):

    raw_input = capture.get_text()
    print_ts(colored("You: ", 'blue') + raw_input)
    entities = capture.get_entities()
    response = Response()

    # filter_by_confidence(entities)
    # not tested, don't use it

    if testing is 1:
        print_ts(str(entities))
        print_ts(str(entities.keys()))

    if len(entities) == 0:
        return "Sorry, I don't know what you mean with " + "'" + capture.get_text() + "'"

    else:
        # fallback to generic response

        if len(entities) == 1:

            if "time" in entities:
                response = TimeResponse(None)
            elif "weather" in entities:
                response = WeatherResponse(None)
            elif "status" in entities:
                response = StatusResponse()
            elif "connection" in entities:
                response = ConnectionResponse()
            elif "note" in entities:
                note_name = nested_execute("note")
                if note_name is not None:
                    response = NoteResponse(note_name)
                    # save the name of the of the note to the memory

        elif len(entities) >= 2:

            if all(k in entities for k in ("weather", "location")):
                location = entities.get("location")[0].get("value")
                response = WeatherResponse(location)
                mem.save_location(location)

            elif all(k in entities for k in ("time", "location")):
                location = entities.get("location")[0].get("value")
                response = TimeResponse(location)
                mem.save_location(location)

            elif all(k in entities for k in ("weather", "reference")):
                location = mem.get_location()
                if location is not None:
                    response = WeatherResponse(location)
                else:
                    if testing is 1:
                        print_ts("Location unknown")

                    location = nested_execute("location")
                    if location is not None:
                        response = WeatherResponse(location)

            elif all(k in entities for k in ("time", "reference")):
                location = mem.get_location()
                if location is not None:
                    response = TimeResponse(location)
                else:
                    if testing is 1:
                        print_ts("Location unknown")

                    location = nested_execute("location")
                    if location is not None:
                        response = TimeResponse(location)

    return response.get_text()


def create_note(recognizer, mic):

    with mic as audio_source:
        say("Ok, I'm listening to your note.")
        playsound('resources/ding.wav')
        rec_audio = recognizer.listen(audio_source)
        playsound('resources/dong.wav')
        capture = rec.recognize_wit(recognizer, rec_audio)

        note_data = capture.get_text()
        print_ts(colored("You: ", 'blue') + note_data)

        date = datetime.datetime.now().strftime("%d-%m-%Y_%H_%M_%S")

        try:
            note = open("notes/note" + date + ".txt", "w")
            note.write(note_data)
            note.close()
            return note.name
        except IOError:
            #say("An error occured whilst saving the note. Try again.")
            return None


def ask_for_location(recognizer, mic):

    num_of_attempts = 3

    with mic as audio_source:
        for x in range(0, num_of_attempts):

            if x is 0:
                say("Where exactly?")
            else:
                say("Can you repeat?")
            playsound('resources/ding.wav')
            rec_audio = recognizer.listen(audio_source)
            playsound('resources/dong.wav')
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

    return None


def nested_execute(type):

    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 0.5
    mic = sr.Microphone()

    if type is "note":
        return create_note(recognizer, mic)

    elif type is "location":
        return ask_for_location(recognizer, mic)

    return None


def print_ts(text):
    time = strftime("%H:%M:%S", gmtime())
    print(colored("[" + time + "] ", 'grey') + text)


colorama_init()
mem = Memory()