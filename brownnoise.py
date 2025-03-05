"""Code for generating brown noise on the Raspberry Pi 5"""

import numpy as np
#import sounddevice as sd
#import soundfile as sf
from scipy.io import wavfile
from scipy.signal import resample
import gpiozero
from time import sleep

AUDIO_FILE = "cats_test.wav" # Import selected audio file for transmission
PWM_PIN = 18
CARRIER_FREQ = 40000
SAMPLERATE = 40000

#def convert_wav(file):
#    data, samplerate = sf.read(AUDIO_FILE)
#    return sf.write("cats_wav_test.wav", data, 40000, subtype='PCM_16')

def load_audio(file):
    samplerate, audio = wavfile.read(file)
    
    # If audio file is stereo, converts to mono by averaging both channels
    if audio.ndim == 2:
        audio = np.mean(audio, axis=1)

    new_len = int(len(audio) * SAMPLERATE / samplerate)
    audio = resample(audio, new_len).astype(np.float32)
    
    # Normalize between -1 and 1
    audio = audio / np.max(np.abs(audio))
    return audio

def am_modulate(audio, carrier_freq, samplerate):
    t = np.linspace(0, len(audio) / samplerate, len(audio))
    carrier = np.sin(2 * np.pi * carrier_freq * t)
    return carrier * audio

audio = load_audio(AUDIO_FILE)
modulated = am_modulate(audio, CARRIER_FREQ, SAMPLERATE)
modulated = (modulated + 1) / 2

signal = gpiozero.PWMOutputDevice(PWM_PIN, frequency=SAMPLERATE)

try:
    print("Directional Audio Laser ON")
    for sample in modulated:
        signal.value = sample
        sleep(1 / SAMPLERATE)
except KeyboardInterrupt:
    print("Stopping laser")
    signal.off()
