import snowboydecoder
import sys
import signal
from light import Light

interrupted = False

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted

if len(sys.argv) != 4:
    print("Error: need to specify model name")
    print("Usage: python demo.py your.model")
    sys.exit(-1)

models = sys.argv[1:]

signal.signal(signal.SIGINT, signal_handler)

sensitivity = [0.5]*len(models)
led = Light(18)
detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)

callbacks = [lambda: led.party(),
	     lambda: led.switch(),
             lambda: snowboydecoder.play_audio_file(snowboydecoder.RANDOM_SONG)]
print('Listening... Press Ctrl+C to exit')


detector.start(detected_callback=callbacks,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()
