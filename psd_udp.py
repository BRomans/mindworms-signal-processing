"""Example program to show how to read a multi-channel time series from LSL."""

from os import remove
from pylsl import StreamInlet, resolve_stream
import numpy as np
import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5001

def bandpower(data, sf, band, window_sec=None, relative=False):
    """Compute the average power of the signal x in a specific frequency band.

    Parameters
    ----------
    data : 1d-array
        Input signal in the time-domain.
    sf : float
        Sampling frequency of the data.
    band : list
        Lower and upper frequencies of the band of interest.
    window_sec : float
        Length of each window in seconds.
        If None, window_sec = (1 / min(band)) * 2
    relative : boolean
        If True, return the relative power (= divided by the total power of the signal).
        If False (default), return the absolute power.

    Return
    ------
    bp : float
        Absolute or relative band power.
    """
    from scipy.signal import welch
    from scipy.integrate import simps
    band = np.asarray(band)
    low, high = band

    # Define window length
    if window_sec is not None:
        nperseg = window_sec * sf
    else:
        nperseg = (2 / low) * sf

    # Compute the modified periodogram (Welch)
    freqs, psd = welch(data, sf, nperseg=nperseg)

    # Frequency resolution
    freq_res = freqs[1] - freqs[0]

    # Find closest indices of band in frequency vector
    idx_band = np.logical_and(freqs >= low, freqs <= high)

    # Integral approximation of the spectrum using Simpson's rule.
    bp = simps(psd[idx_band], dx=freq_res)

    if relative:
        bp /= simps(psd, dx=freq_res)
    return bp

def main():
    # first resolve an EEG stream on the lab network
    print("looking for an EEG stream...")
    streams = resolve_stream('type', 'EEG')

    # create a new inlet to read from the stream

    inlet = StreamInlet(streams[0])
    print()

    buffer = []
    max_samples = 500
    channel = 0

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        # get a new sample (you can also omit the timestamp part if you're not
        # interested in it)
        sample, timestamp = inlet.pull_sample()
        # print(timestamp, sample)

        # SMR  channel 9 + Beta channel 22
        smr_ch_9 = 9
        beta_ch_22 = 22

        buffer.append(sample[smr_ch_9])
        buffer.append(sample[beta_ch_22])
        if len(buffer)>max_samples:
            buffer.pop(0)
            bp_smr = bandpower(buffer[0], 100, [12, 15], relative=True)
            bp_beta = bandpower(buffer[1], 100, [15, 18], relative=True)
            msg = str(bp_smr)
            print(bp_smr)
            print(bp_beta)
            sock.sendto(msg.encode('utf_8'), (UDP_IP, UDP_PORT))

        
if __name__ == '__main__':
    main()