"""Example program to show how to read a multi-channel time series from LSL."""

from os import remove
from pylsl import StreamInlet, resolve_stream
import time
import numpy as np
import socket
from datetime import datetime

UDP_IP = "127.0.0.1"
UDP_PORT = 1048

now = datetime.now()
print(now)
file = open("radhika_6.txt","w")

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

    # SMR  channel 9 + Beta channel 22
    smr_ch = 9
    beta_ch =32 

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    TIMER = 30

    baseline_smr = []
    baseline_beta = []
    t_end = time.time() + 30
    
    #calculating baseline 
    while time.time() < t_end:
        sample, timestamp = inlet.pull_sample()
        baseline_smr.append(sample[smr_ch])
        baseline_beta.append(sample[beta_ch])
    
    #calculating band power
    bs_smr_bp = bandpower(baseline_smr, 512, [12,15], relative=True)
    bs_beta_bp = bandpower(baseline_beta, 512, [15,18], relative=True)
    bs_smr = np.mean(bs_smr_bp)
    bs_beta = np.mean(bs_beta_bp)

    # print("Your SMR baseline : ", bs_smr)
    # print("Your Beta baseline : ", bs_beta)

    while True:
        # get a new sample (you can also omit the timestamp part if you're not
        # interested in it)
        sample, timestamp = inlet.pull_sample()
        # print(timestamp, sample)

        buffer.append(sample[smr_ch])
        buffer.append(sample[beta_ch])
        if len(buffer) > max_samples:
            buffer.pop(0)
            bp_smr = bandpower(buffer, 512, [12, 15], window_sec=2, relative=True)
            bp_beta = bandpower(buffer, 512, [15, 18], window_sec=2, relative=True)
            bp_smr_diff = float(bp_smr - bs_smr)
            bp_beta_diff = float(bp_beta - bs_beta)
            # file.write(bp_smr_diff, bp_beta_diff)
            bp_smr_diff = bp_smr_diff * 100000000
            bp_beta_diff = bp_beta_diff * 100000000
            print("SMR diff: ", bp_smr_diff)
            print("beta diff: ", bp_beta_diff)
            msg = "{:.10f}".format(bp_beta_diff) + " " + "{:.10f}".format(bp_smr_diff)
            file.write(msg)
            #msg += ","
            sock.sendto(msg.encode('utf_8'), (UDP_IP, UDP_PORT))
            file.write(msg)
            msg += "\r\n"
            
        
if __name__ == '__main__':
    main()