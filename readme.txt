On Debian-derived Linux distributions we need to install PyAudio using APT in a terminal:

$ sudo apt-get install python-pyaudio python3-pyaudio

On macOS, install PortAudio using Homebrew and then install PyAudio using Pip: 

$ brew install portaudio
$ pip install pyaudio

On other POSIX-based systems, install the portaudio19-dev and python-all-dev packages using a package manager of your choice, and then install PyAudio using Pip: 

$ pip install pyaudio



Other dependencies 

From this point the installation of the other dependencies should be straight forward. We need to install all packages listed in the requirements file. 

$ pip install -r requirements.txt



Quick Start Tutorial

If the installation is successful, we are now able to start the application by running the following bash script:

	$ ./start.sh 

The application will perform a quick status check at the beginning, following the program awaiting the catchphrase. We can say "hey Pi" to access the main functionality of the application. After the catchphrase was detected successfully, we are now able to ask the device simple questions. Some of the possible commands are listed below:
- What’s the time in (London | there)?
- What’s the weather like (in London | there)?
- Am I connected to the Internet?
- What’s the status?
- Take a note

After every successful or unsuccessful command, the application is awaiting further instructions. To cancel that, we can say “stop” and the device will return to its original state. 
	
Additionally, we developed commands that manage the LED light that we connected to the Raspberry Pi as well as produce playback of a random .wav file that is stored locally out of the speakers. These commands are relying solely on Snowboy as they didn’t require an internet connection as all of the Snowboy hotword models are stored locally. The listener can be executed with the following command: 
	
	$ ./startled.sh
 
From there the Snowboy listener will be triggered by three hotwords:
- “Light Party” - which is making the LED light flash a couple of times
- “Light Switch” - which switches the LED on/off
- “Play Some Music” - plays a random song from the resources/music folder

