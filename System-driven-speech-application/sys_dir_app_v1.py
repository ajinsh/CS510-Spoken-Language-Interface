"""
A Patient Information command-line utility using Google Speech API and Text-to-Speech API 
It is a system-directed dialogue flow where the system asks the user a set of questions 
and the user gives appropriate answers to it.

API Used :- PyAudio, Google Speech API,pyTTSx3

Functionality implemented :- Speech to text

"""


import pyaudio
import wave
import sys
import time
import base64
import googleapiclient.discovery
import io
import os
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types


CHUNK = 1024
WAVE_OUTPUT_FILENAME = "op"
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 5

pyL = ["Q101.wav","Q2.wav","Q3.wav","Q4.wav","Q5.wav"]

mes = ["What's the patient's temperature in Fahrenheit?", "Whats the patient's systolic blood pressure?","Whats the patient's diastolic blood pressure?","What's the patient's pulse rate?","Whats the patient's pain-level on a scale of 1 to 10?"]

trans = ["","","","",""]

client = speech.SpeechClient()

for index,x in enumerate(pyL):
    wf = wave.open(x, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True)

    data = wf.readframes(CHUNK)

    print(mes[index])      

    while len(data) > 0:
        stream.write(data)
        time.sleep(0.0155)  
        data = wf.readframes(CHUNK)

    wf.close()
    stream.stop_stream()
    stream.close()
    p.terminate()


    while(True):  

        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

        print("* recording")

        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        print("* done recording")

        stream.stop_stream()
        stream.close()
        p.terminate()

        WAVE_OUTPUT_FILENAME = WAVE_OUTPUT_FILENAME+"_"+str(index+1)+".wav" 

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
      
        speech_file= os.path.join(
                os.path.dirname(__file__),
                WAVE_OUTPUT_FILENAME)

         # Loads the audio into memory
        with io.open(speech_file, 'rb') as audio_file:
                content = audio_file.read()
                audio = types.RecognitionAudio(content=content)

        config = types.RecognitionConfig(
                encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code='en-US')

            # Detects speech in the audio file
        response = client.recognize(config, audio)

        for result in response.results:
            trans[index]=result.alternatives[0].transcript
            print(trans[index])
            
            # [END speech_quickstart]
       

        if (index==0):
            try:
                if(-400<=int(trans[index])<=215):
                    tempt =int(trans[index])
                    break
            except ValueError:
                print("Enter a valid temperature between -400 and 215")
            except:
                print("System cannot read")

        if (index==1):        
            try:
                if(70<=int(trans[index])<=190):
                    sbp =int(trans[index])
                    break
            except:
                print("Enter a valid reading between 70-190")
        
        if (index==2):        
            try:
                if(40<=int(trans[index])<=100):
                    dbp =int(trans[index])
                    break
            except ValueError:
                print("Enter a valid reading between 40-100")
 
        
        if (index==3):                
            try:
                if(70<=int(trans[index])<=100):
                    pulr =int(trans[index])

                    break
            except ValueError:
                print("Enter a valid pulse rate between 70-100")
              


        if (index==4):            
            try:
                if(1<=int(trans[index])<=10):
                    painl =int(trans[index])
                    break
            except ValueError:
                print("Enter a valid pain level between 1 to 10")

        os.remove(WAVE_OUTPUT_FILENAME)
        WAVE_OUTPUT_FILENAME = "op"        
                
    #print(index)
    #print("EOF")            
    WAVE_OUTPUT_FILENAME = "op"

print("Here's the patient summary")
print("The patient's recorded temperature is "+trans[0])
print("The patient's recorded systolic blood pressure is "+trans[1])
print("The patient's recorded diastolic blood pressure is "+trans[2])
print("The patient's recorded pulse rate is "+trans[3])
print("The patient's recorded pain level is "+trans[4])





