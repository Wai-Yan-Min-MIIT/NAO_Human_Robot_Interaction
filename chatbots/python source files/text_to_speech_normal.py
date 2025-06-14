from naoqi import ALProxy
tts = ALProxy("ALTextToSpeech", "192.168.2.20", 9559)
tts.say("Hello, world!")