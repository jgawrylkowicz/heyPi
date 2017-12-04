import time
from respond import Response
from respond import TimeResponse
from respond import WeatherResponse


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

    print("You: " + command.get_text())

    entities = command.get_entities()

    if testing is 1:
        print(str(entities))

    if len(entities) == 0:
        return "Sorry, I don't know what you mean with '" + command.get_text() + "'"

    else:
        keys = entities.keys()
        # fallback to generic response
        response = Response

        if len(entities) == 1:

            if "time" in keys:
                response = TimeResponse(None)
            elif "weather" in keys:
                response = WeatherResponse(None)

        elif len(entities) == 2:
            keys = entities.keys()
        
            if "weather" and "location" in keys:
                # entities["location"]["value"]
                # location = command.get_entities().get("location").get("value")
                location = "Vienna"
                response = WeatherResponse(location)

            elif "time" and "location" in keys:
                location = "Vienna"
                #location = command.get_entities().get("location").get("value")
                response = TimeResponse(location)

        return response.get_text()

