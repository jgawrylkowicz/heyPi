import time
import datetime
import pyowm

testing = 1
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
        location = ""
        time = datetime.datetime.now()

        if self.location is not None:
            # check for time at location
            time = datetime.datetime.now()
            location = " in " + self.location

        if time.hour is 0:
            return str("It is now " + str(time.minute)) + " minutes after midnight" + location
        else:
            return str("It is now " + str(time.hour) + ":" + str(time.minute)) + location


class WeatherResponse(Response):
    open_weather_api = "ab91afe8558fe27c9a17ef07622fa3c1"
    owm = pyowm.OWM(open_weather_api)

    def __init__(self, location):
        Response.__init__(self)
        self.location = location

    def get_text(self):
        # observation = current weather
        # forecast maybe later
        if self.location is not None:
            observation = self.owm.weather_at_place(self.location)
            weather = observation.get_weather()

            temp = weather.get_temperature("celsius")
            if testing is 1:
                print(weather)

            return "It is now " + str(temp.temp) + "degrees celsius in " + self.location


class StatusResponse(Response):
    def __init__(self):
        Response.__init__(self)

    def get_text(self):
        # connection to internet, ip address
        return ""


class Capture:
    def __init__(self, text, entities):
        self.text = text
        self.entities = entities  # dict
        self.time_recorded = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

    def get_text(self):
        return self.text

    def get_entities(self):
        return self.entities