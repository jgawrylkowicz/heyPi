from execute import Capture
import speech_recognition as sr
# Wit.ai is used for the actual language understanding. Is not only returns transcribed audio, but
# but also the intent or keywords of the command, so-called entities, which can be configured on
# their website.
# e.g. "What time is it"  Entity:time
# e.g. "What time is it in Vienna" Entity:time, location


# TODO need to change the return variables
def recognize_wit(recognizer, audio):
    if audio is not None:
        wit_ai_key = "ETJDE6YJR44VJT2X4OGDYOLQGGVIWE65"
        try:
            api_response = recognizer.recognize_wit(audio, key=wit_ai_key, show_all=True)
            capt = Capture(api_response.get('_text'), api_response.get('entities'))
            return capt

        except sr.UnknownValueError:
            return "Wit.ai could not understand audio"
        except sr.RequestError as e:
            return "Could not request results from Wit.ai service; {0}".format(e)
    else:
        return "Sorry, I didn't catch that"


# As mentioned in feedback I have implemented an offline recognition via Sphinx, for the sole
# purpose to recognize the catchphrase from the audio.

def recognize_sphinx(recognizer, audio):
    if audio is not None:
        try:
            api_response = recognizer.recognize_sphinx(audio, language="en-US")
            capt = Capture(api_response.get('_text'), "")

            return capt

        except sr.UnknownValueError:
            return "Sphinx could not understand audio"
        except sr.RequestError as e:
            return "Sphinx error; {0}".format(e)


def test_wit():
    # TODO IOERROR
    audio_file_path = "resources/test.flac"
    r = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as source:
        audio_file = r.record(source)
        return recognize_wit(r, audio_file)