"""Code for generating brown noise on the Raspberry Pi 5"""

import numpy as np
import sounddevice as sd

def generate_white_noise(duration, sample_rate):
    """Generates white noise"""

    num_samples = duration * sample_rate
    noise = np.random.randn(int(num_samples))

    return noise

def generate_brown_noise(duration, sample_rate):
    """Generates brown noise"""

    # Collect samples
    num_samples = duration * sample_rate
    
    # Generate white noise
    white_noise = np.random.randn(int(num_samples))
    
    # Integrate white noise to get brown noise
    brown_noise = np.cumsum(white_noise)

    # Normalize to prevent clipping
    brown_noise = brown_noise / np.max(np.abs(brown_noise))

    print(f"Playing {duration} seconds of brown noise.")
    sd.play(brown_noise, samplerate=sample_rate)
    sd.wait()

generate_brown_noise(5, 44100)