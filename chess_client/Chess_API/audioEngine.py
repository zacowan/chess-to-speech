'''
Created on Oct 16, 2021
Most of this file came from : https://stackoverflow.com/a/6743593
It was altered and repurposed by Legacy for the purposes of this project
'''
from sys import byteorder
from array import array
from struct import pack
import pyaudio
import wave
import theMain
import restService

THRESHOLD = 1800 # Quiteness threshold adjust this to adjust min volume required for End Point Detection
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
RATE = 44100

#Future FEATURE: While the User is speaking Andy stops talking or goes low volume

def setupAudioEngine():
    count = 0
    while not theMain.isClosed():
        file_path= "UserSpeech" + str(count)+".wav"
        record_to_file(file_path)
        restService.sendUserAudio(file_path) #send to Andy Api
        
        #This is to create a buffer of .wav files, so that they aren't deleted immediately
        count+=1
        if count >=10:
            count=0
        
        
def is_silent(snd_data):
    "Returns 'True' if below the 'silent' threshold"
    return max(snd_data) < THRESHOLD

def normalize(snd_data):
    "Average the volume out"
    MAXIMUM = 16384
    times = float(MAXIMUM)/max(abs(i) for i in snd_data)

    r = array('h')
    for i in snd_data:
        r.append(int(i*times))
    return r

def trim(snd_data):
    "Trim the blank spots at the start and end"
    def _trim(snd_data, reverse): #reverse is a decrease to threshold as words can end quite which would cause them to get cut off for not meeting threshold
        snd_started = False
        r = array('h')

        for i in snd_data:
            if not snd_started and abs(i)>THRESHOLD-reverse:
                snd_started = True
                r.append(i)

            elif snd_started:
                r.append(i)
        return r

    # Trim to the left
    snd_data = _trim(snd_data,0)

    # Trim to the right
    snd_data.reverse()
    snd_data = _trim(snd_data,600)
    snd_data.reverse()
    return snd_data

def add_silence(snd_data, seconds):
    "Add silence to the start and end of 'snd_data' of length 'seconds' (float)"
    silence = [0] * int(seconds * RATE)
    r = array('h', silence)
    r.extend(snd_data)
    r.extend(silence)
    return r

def record():
    """
    Record a word or words from the microphone and 
    return the data as an array of signed shorts.

    Normalizes the audio, trims silence from the 
    start and end, and pads with 0.5 seconds of 
    blank sound to make sure VLC et al can play 
    it without getting chopped off.
    """
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=1, rate=RATE,
        input=True, output=True,
        frames_per_buffer=CHUNK_SIZE)

    num_silent = 0
    num_len = 0
    snd_started = False

    r = array('h')

    while not theMain.isClosed():
        # little endian, signed short
        snd_data = array('h', stream.read(CHUNK_SIZE))
        if byteorder == 'big':
            snd_data.byteswap()
        r.extend(snd_data)

        silent = is_silent(snd_data)

        if silent and snd_started: #Increments silent counter
            num_silent += 1
            num_len+=1
        elif not silent and snd_started: # resets silent counter
            num_silent = 0
            num_len+=1
        elif not silent and not snd_started:# if it detects audio for the first time
            snd_started = True

        if snd_started and (num_silent > 60 or num_len >700): #Ending conditions Silent for more than 50 iterations and total audio grater than 700 iterations
            break

    sample_width = p.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    p.terminate()
    #del r[0:8000] # not working hot fix, left here for future experiments
    r = normalize(r)  #Normalizes audio - "Average the volume out"
    r = trim(r) #trims the silence from the start and end
    r = add_silence(r, 0.5) #adds .5 seconds of silence to the start and end
    return sample_width, r

#Generate a .wav file based on user speech (end point detection included)
def record_to_file(path):
    "Records from the microphone and outputs the resulting data to 'path'"
    sample_width, data = record()
    data = pack('<' + ('h'*len(data)), *data)

    wf = wave.open(path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()

def playAudio(filepath):
    #define stream chunk   
    chunk = 1024  
    
    #open a wav format music  
    f = wave.open(filepath,"rb")  
    #instantiate PyAudio  
    p = pyaudio.PyAudio()  
    #open stream  
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                    channels = f.getnchannels(),  
                    rate = f.getframerate(),  
                    output = True)  
    #read data  
    data = f.readframes(chunk)  
    
    #play stream  
    while data and not theMain.isClosed():  
        stream.write(data)  
        data = f.readframes(chunk)  
    
    #stop stream  
    stream.stop_stream()  
    stream.close()  
    
    #close PyAudio  
    p.terminate()
    
    
    
#For testing purposes
#if __name__ == '__main__':
#    playAudio('UserSpeech0.wav')
