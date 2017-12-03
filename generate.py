import time
import datetime


# I have split responses into subclasses. I don't know if it's a good idea or not,
# so you are free to change it.

class Response:
    # A dictionary is needed for generating responses
    def __init__(self):
        self.time_generated = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())


class TimeResponse(Response):
    def __init__(self, location):
        Response.__init__(self)
        self.location = location

    def get_text(self):
        if self.location is None:
            now = datetime.datetime.now()
            return str("It is now " + str(now.hour) + ":" + str(now.minute))


class Capture:
    def __init__(self, text, entities):
        self.text = text
        self.entities = entities  # dict
        self.time_recorded = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

    def get_text(self):
        return self.text

    def get_entities(self):
        return self.entities