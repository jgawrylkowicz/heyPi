import time
import datetime
import pyowm
import pytz
from geopy import geocoders
from tzwhere import tzwhere
#import urllib2
import socket

testing = 0
# I have split responses into subclasses. I don't know if it's a good idea or not,
# so you are free to change it.


class Response:
    # A dictionary is needed for generating responses
    def __init__(self):
        self.time_generated = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

    def get_text(self):
        pass


class TimeResponse(Response):
    def __init__(self, location):
        Response.__init__(self)
        self.location = location

    def get_text(self):

        def get_location(loc_string):
            g = geocoders.Nominatim()
            return g.geocode(loc_string)

        def get_timezone(lat, lng):
            w = tzwhere.tzwhere()
            z = w.tzNameAt(lat, lng)
            tz = pytz.timezone(z)
            return tz

        location = ""
        time = datetime.datetime.now()

        if self.location is not None:
            # check for time at location
            loc = get_location(self.location)
            tz = get_timezone(loc.latitude, loc.longitude)
            time = datetime.datetime.now(tz)
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
        if location is None:
            # pull the standard location from a config file
            self.location = "Vienna"
        else:
            self.location = location

    def get_text(self):

        # more entries to come
        def get_status(s):
            return {
                "Clouds": "The sky is overcast.",
                "Rain": "It's raining.",
                "Clear": "The sky is clear.",
                "Snow": "It's snowing.",
                "Thunderstorm": "There is a storm outside. Be safe.",
                "Drizzle": "Watch out for fog and drizzle"
            }.get(s, "")

        response = ""
        # observation = current weather
        # forecast maybe later
        if self.location is not None:
            observation = self.owm.weather_at_place(self.location)
            weather = observation.get_weather()

            temp = weather.get_temperature("celsius")
            current_temp = int(round(temp.get("temp")))
            response += "It is now " + str(current_temp) + " degrees celsius in " + self.location + ". "

            status = weather.get_status()
            response += get_status(status)

            return response


class StatusResponse(Response):
    def __init__(self):
        Response.__init__(self)

    def get_text(self):
        # connection to internet, ip address

        response = ""

        if internet_on() is 1:
            response += "I'm connected to the internet. "
            if get_ip() is not None:
                response += "My ip address is " + get_ip()
            else:
                response += "But I can't determine the ip address."
        else:
            # probably never called
            response += "Sorry, I can't connect to the internet. "
            response += get_ip()

        return response


def internet_on():
    try:
        # ping google.com
        urllib2.urlopen('http://216.58.192.142', timeout=1)
        return 1
    except urllib2.URLError as err:
        return 0


def get_ip():
    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        return ip
    except socket.gaierror as err:
        return None
