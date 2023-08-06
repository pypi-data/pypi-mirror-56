#!/usr/bin/env python3
'''
Created on 16 Nov 2019

@author: julianporter
'''
import rubberband 
from sound import wavfile


nFrames = None
rate = None
bitrate = None
stream = None

with wavfile("slugs.wav",rw='r') as wav:
    rate=wav.rate
    bitrate=rate*16
    stream = wav.read()

nFrames=len(stream)
oldDuration=nFrames/rate

newDuration=4
ratio=newDuration/oldDuration
print(f'Ratio is {ratio}')

out=rubberband.stretch(stream,rate=bitrate,ratio=ratio,crispness=5,formants=True)

with wavfile("slugs_st.wav",rw='w',rate=rate) as f:
    f.write(out)


  



    
    
    
    
