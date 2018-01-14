import speech_recognition as sr
import recognize as rec
import time
import datetime
from respond import Response
from respond import TimeResponse
from respond import WeatherResponse
from respond import StatusResponse
from respond import ConnectionResponse
from time import gmtime, strftime
from colorama import init as colorama_init
from termcolor import colored
from voice import say

testing = 0  # additional command prints
additionalLn = 0 # additional line for user input
same_day_notes = 0 # same date note helper

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

    raw_input = capture.get_text()
    print_ts(colored("You: ", 'blue') + raw_input)
    entities = capture.get_entities()
    response = Response()
   # entitydict(entities, capture)


    if testing is 1:
        print_ts(str(entities))
        print_ts(str(entities.keys()))

    if additionalLn == 1:  # true when the command requires an additional line from the user
        create_note(raw_input)
        #response = NoteResponse()
        say("Your note has been successfully made.")
    else:

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
                    goAgain()


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

                        location = nested_execute("location")
                        if location is not None:
                            response = WeatherResponse(location)

                elif all(k in entities for k in ("time", "reference")):
                    location = ref.get_location()
                    if location is not None:
                        response = TimeResponse(location)
                    else:
                        if testing is 1:
                            print_ts("Location unknown")

                        location = nested_execute("location")
                        if location is not None:
                            response = TimeResponse(location)

    return response.get_text()


def create_note(note_data):

    global additionalLn, same_day_notes

    date = datetime.datetime.now().strftime("%d-%m-%Y")
    if same_day_notes > 0:

        note = open("Note" + date + "_" + str(same_day_notes) + ".txt", "w")
    elif same_day_notes == 0:
        note = open("Note" + date + ".txt", "w")

    note.write(note_data)
    note.close()
    same_day_notes += 1
    additionalLn = 0
    return

def goAgain():
    global additionalLn
    additionalLn = 1
    return None

def nested_execute(type):

    num_of_attemps = 3

    for x in range(0, num_of_attemps):

        if x is 0:
            say("Where exactly?")
        else:
            say("Can you repeat?")

        recognizer = sr.Recognizer()
        recognizer.pause_threshold = 0.5
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

    return None


def print_ts(text):
    time = strftime("%H:%M:%S", gmtime())
    print(colored("[" + time + "] ", 'grey') + text)


colorama_init()
ref = Reference()