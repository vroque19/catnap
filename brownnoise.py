"""Code for generating brown noise on the Raspberry Pi 5"""

import numpy as np
import sounddevice as sd

def generate_white_noise(duration, sample_rate):
    """Generates white noise"""

    num_samples = duration * sample_rate
    noise = np.random.randn(int(num_samples))

    return noise

def generate_brown_noise(duration, sample_rate, volume):
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

def generate_brown_noise_buffer(buffer_size=44100, volume=0.3):
    """Generates brown noise"""
    
    # Generate white noise
    white_noise = np.random.randn(int(buffer_size))
    
    # Integrate white noise to get brown noise
    brown_noise = np.cumsum(white_noise)

    # Normalize to prevent clipping
    brown_noise = brown_noise / np.max(np.abs(brown_noise))

    # Apply crossfade to prevent pops
    fade_samples = int(buffer_size * 0.1)
    fade_in = np.linspace(0, 1, fade_samples)
    fade_out = np.linspace(1, 0, fade_samples)

    brown_noise[:fade_samples] *= fade_in
    brown_noise[-fade_samples:] *= fade_out
    
    return np.clip(brown_noise, 0, 100).astype(int)

def stream_brown_noise(volume = 0.3, sample_rate = 44100):
    """Streams brown noise until Ctrl+Z is pressed"""
    
    buffer_size = 192000
    noise_buffer = generate_brown_noise_buffer(buffer_size=buffer_size, volume=volume)
    
    def callback(outdata, frames, time, status):
        if status:
            print(status)
        outdata[:] = noise_buffer[:frames].reshape(-1, 1)

    with sd.OutputStream(callback=callback, samplerate=sample_rate, channels=1, blocksize=buffer_size):
        print("Streaming brown noise...to stop press Ctrl+Z")
        while True:
            pass


#generate_brown_noise(20, 44100)
stream_brown_noise(0.5)