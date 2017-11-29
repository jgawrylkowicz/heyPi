import speech_recognition as sr

WIT_AI_KEY = "ETJDE6YJR44VJT2X4OGDYOLQGGVIWE65"
trigger = "hey"

# saving the last queries / commands for later use
# new_dict = dict()


# TODO use pocketsphinx for offline recognition
# capture the voice command and recognize it via wit.ai
def recognize(rec_audio):
    try:
        return r.recognize_wit(rec_audio, key=WIT_AI_KEY)
    except sr.UnknownValueError:
        print("Wit.ai could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Wit.ai service; {0}".format(e))


# listen to voice commands
def listen(audio_source):
    while 1:
        audio = r.listen(audio_source)
        command = recognize(audio)

        print(command)

        # if r.recognize_wit(audio, key=WIT_AI_KEY) == trigger:
        #     # Trigger recognized, listening to the command
        #     recognize(audio)
        # else:
        #     # Voice captured, but the trigger wasn't recognized
        #     print("Trigger not recognized")


r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    listen(source)



