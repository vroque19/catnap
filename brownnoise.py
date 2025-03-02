"""Code for generating brown noise on the Raspberry Pi 5"""

import numpy as np

def generate_white_noise(duration, sample_rate):
    """Generates white noise"""

    noise = numpy.random.randn(int(duration * sample_rate))

    return noise