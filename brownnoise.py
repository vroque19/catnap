"""Code for generating brown noise on the Raspberry Pi 5"""

import numpy as np
#import sounddevice as sd
from scipy.io import wavfile
from scipy.signal import resample
import gpiozero
from time import sleep

AUDIO_FILE = "cats_test.wav" # Import selected audio file for transmission
PWM_PIN = 18
CARRIER_FREQ = 40000
SAMPLERATE = 40000

def load_audio(file):
    samplerate, audio = wavfile.read(file)
    new_len = int(len(audio) * SAMPLERATE / samplerate)
    audio = resample(audio, new_len).astype(np.float32)
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
