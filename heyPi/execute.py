import main
import generate as gen



testing = 1  # additional command prints

# Executes a 'Command' object. At this time it checks if a command contains a specific
# string. If no entities have been found by wit.ai, the command cannot be processed.


def execute(command):

    print("You: " + command.get_text())
    if testing is 1:
        print("Entities: " + str(command.get_entities()))

    entities = command.get_entities()
    for entities in command.get_entities():
        print entities
    if len(entities) == 0:
        main.say("Sorry, I don't know what you mean with '" + command.get_text() + "'")

    else:
        keys = entities.keys()
        # fallback to generic response
        response = gen.Response

        if len(entities) == 1:

            if "time" in keys:
                response = gen.TimeResponse(None)
            elif "weather" in keys:
                response = gen.WeatherResponse(None)

        elif len(entities) == 2:
            keys = entities.keys()

            if "weather" and "location" in keys:
                response = gen.TimeResponse(None)

            elif "time" and "location" in keys:
                response = gen.TimeResponse(None)

        main.say(response.get_text())

