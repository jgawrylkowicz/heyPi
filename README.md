# heyPi

A CLI voice assistent written in Python based on the SpeechRecognition package.  


## Features

* Text-to-speech: Thanks to Google’s text-to-speech API the device is able to read out responses to the user. 
* Audio feedback: The beginning and the end of a audio capture are represented by simple sounds. 
* Catch-phrase via Snowboy: Thanks to the snowboy hotword detection engine we were able to implement the catchphrase functionality efficiently. The device will not start listening to the command until the phrase “hey Pi” has been caught. 
* References: We have implemented a simple solution to referencing past commands. 
* Missing Information: Some commands may require additional information if the provided one hasn't been specific enough. In that case, the device will ask for the missing information.  
* Time (in a location): The user can ask the device for the current time in a location (optional). 
* Weather (in a location): The user can ask the device for the current weather in a location (optional). 
* System status: The user is able to get information about the current device status: connection to the internet, connection to the API, the current IP address
* Creating notes: It’s possible to create and save notes. The device will transcribe the audio and save it as a simple text file on the local storage. After the device recognizes that the user wants to take a note it will prompt the user once more with a nested command which is able to take the user message and save it in the .txt file. 

## Installation 

From this point the installation of the other dependencies should be straight forward. 
We need to install all packages listed in the requirements file.

```bash
$ pip install -r requirements.txt
```

## Quick Start

If the installation is successful, we are now able to start the application by running the following bash script:

```bash
$ ./start.sh 
```

The application will perform a quick status check at the beginning, following the program awaiting the catchphrase. We can say "hey Pi" to access the main functionality of the application. After the catchphrase was detected successfully, we are now able to ask the device simple questions. Some of the possible commands are listed below:
* What’s the time in (London | there)?
* What’s the weather like (in London | there)?
* Am I connected to the Internet?
* What’s the status?
* Take a note

After every successful or unsuccessful command, the application is awaiting further instructions. 
To cancel that, we can say “stop” and the device will return to its original state. 
	
Additionally, we developed commands that manage the LED light that we connected to the Raspberry Pi 
as well as produce playback of a random .wav file that is stored locally out of the speakers. 
These commands are relying solely on Snowboy as they didn’t require an internet connection 
as all of the Snowboy hotword models are stored locally. The listener can be executed with the following command: 

```bash
$ ./startled.sh
```

From there the Snowboy listener will be triggered by three hotwords:
* “Light Party” - which is making the LED light flash a couple of times
* “Light Switch” - which switches the LED on/off
* “Play Some Music” - plays a random song from the resources/music folder

## Screenshots

![alt text](https://github.com/jgawrylkowicz/heyPi/blob/final/img/1.png "1")
![alt text](https://github.com/jgawrylkowicz/heyPi/blob/final/img/2.png "2")
