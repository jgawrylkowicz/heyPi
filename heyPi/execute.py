import time
from respond import Response
from respond import TimeResponse
from respond import WeatherResponse
from respond import StatusResponse
from time import gmtime, strftime
from colorama import init as colorama_init
from termcolor import colored

colorama_init()

testing = 0  # additional command prints

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


def execute(command):

    print_ts(colored("You: ", 'blue') + command.get_text())
    entities = command.get_entities()

    if testing is 1:
        print_ts(str(entities))

    if len(entities) == 0:
        return colored("Sorry, I don't know what you mean with ", 'red') + "'" + command.get_text() + "'"

    else:
        keys = entities.keys()
        # fallback to generic response
        response = Response

        if len(entities) == 1:

            if "time" in keys:
                response = TimeResponse(None)
            elif "weather" in keys:
                response = WeatherResponse(None)
            elif "status" in keys:
                response = StatusResponse()

        elif len(entities) == 2:
            keys = entities.keys()

            if "weather" and "location" in keys:
                location = command.get_entities().get("location")[0].get("value")
                response = WeatherResponse(location)

            if "time" and "location" in keys:
                location = command.get_entities().get("location")[0].get("value")
                response = TimeResponse(location)

        return response.get_text()


def print_ts(text):
    time = strftime("%H:%M:%S", gmtime())
    print colored("[" + time + "] ", 'grey') + text