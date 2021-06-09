import numpy as np
import sys
sys.argv=['']
del sys
import getopt
import time
import os
from random import random as rand
from pylsl import StreamInfo, StreamOutlet, local_clock
#os.chdir('C://Users//user//Documents//UT_Interaction_Technology//J1//q4//BCI')
#eeg_data = "example_output_eeg.txt"

from pylsl import StreamInlet, resolve_stream


def main():
    # first resolve an EEG stream on the lab network
    print("looking for an EEG stream...")
    streams = resolve_stream('type', 'EEG')

    # create a new inlet to read from the stream
    inlet = StreamInlet(streams[0])
    
    while True:
        n=0;
        channel1=[]
        channel2=[]
        channel3=[]
        channel4=[]
        while (n<100):
            # get a new sample (you can also omit the timestamp part if you're not
            # interested in it)
            sample, timestamp = inlet.pull_sample()
            #print(timestamp, sample)
            ch1=sample[0]
            ch2=sample[1]
            ch3=sample[2]
            ch4=sample[3]
            
            #print(ch1)
            #data = np.loadtxt(sample)
            channel1.append(ch1)
            channel2.append(ch2)
            channel3.append(ch3)
            channel4.append(ch4)
            n+=1
        
        print(channel1)
        import matplotlib.pyplot as plt
        import seaborn as sns
        sns.set(font_scale=1.2)
        
        #10 ms between each print

        sf = 100
        time=np.arange(100)
        #time = np.arange(data.size) / sf
        fig, ax = plt.subplots(1, 1, figsize=(12, 4))
        plt.plot(time, channel1, lw=1.5, color='k')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Voltage')
        plt.xlim([time.min(), time.max()])
        plt.title('Sample EEG')
        sns.despine()
        
        
        fig, ax = plt.subplots(1, 1, figsize=(12, 4))
        plt.plot(time, channel2, lw=1.5, color='k')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Voltage')
        plt.xlim([time.min(), time.max()])
        plt.title('Sample EEG')
        sns.despine()
        
        from scipy import signal
        # Define window length (4 seconds)
        win = 4 * sf
        freqs, psd = signal.welch(channel1, sf, nperseg=win)
        # Plot the power spectrum
        sns.set(font_scale=1.2, style='white')
        plt.figure(figsize=(8, 4))
        plt.plot(freqs, psd, color='k', lw=2)
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Power spectral density (V^2 / Hz)')
        plt.ylim([0, psd.max() * 1.1])
        plt.title("Welch's periodogram")
        plt.xlim([0, freqs.max()])
        sns.despine()
        
        freqs2, psd2 = signal.welch(channel2, sf, nperseg=win)
        # Plot the power spectrum
        sns.set(font_scale=1.2, style='white')
        plt.figure(figsize=(8, 4))
        plt.plot(freqs2, psd2, color='k', lw=2)
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Power spectral density (V^2 / Hz)')
        plt.ylim([0, psd.max() * 1.1])
        plt.title("Welch's periodogram")
        plt.xlim([0, freqs.max()])
        sns.despine()
        
        
        # Define SMR lower and upper limits
        low, high = 12.5, 15.5
        
        # Find intersecting values in frequency vector
        idx_delta = np.logical_and(freqs >= low, freqs <= high)
        idx_delta2 = np.logical_and(freqs2 >= low, freqs2 <= high)
        # Plot the power spectral density and fill the SMR area
        plt.figure(figsize=(7, 4))
        plt.plot(freqs, psd, lw=2, color='k')
        plt.fill_between(freqs, psd, where=idx_delta, color='skyblue')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Power spectral density (uV^2 / Hz)')
        plt.xlim([0, 17])
        plt.ylim([0, psd.max() * 1.1])
        plt.title("Welch's periodogram")
        sns.despine()
        
        plt.figure(figsize=(7, 4))
        plt.plot(freqs2, psd2, lw=2, color='k')
        plt.fill_between(freqs2, psd2, where=idx_delta, color='skyblue')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Power spectral density (uV^2 / Hz)')
        plt.xlim([0, 17])
        plt.ylim([0, psd2.max() * 1.1])
        plt.title("Welch's periodogram")
        sns.despine()
        from scipy.integrate import simps
        
        
        # Frequency resolution
        freq_res = freqs[1] - freqs[0]  # = 1 / 4 = 0.25
        freq_res2 = freqs2[1] - freqs2[0]  # = 1 / 4 = 0.25        
        smr_power = simps(psd[idx_delta], dx=freq_res)
        print('Absolute SMR power of ch 1: %.3f uV^2' % smr_power)
        
        smr_power2 = simps(psd2[idx_delta2], dx=freq_res2)
        print('Absolute SMR power of ch 2: %.3f uV^2' % smr_power2)
        
        
        # Relative smr power (expressed as a percentage of total power)
       # total_power = simps(psd, dx=freq_res)
        #smr_rel_power = smr_power / total_power
        #print('Relative smr power: %.3f' % smr_rel_power)
        
        #goal: give every second one output.
        
        break;
if __name__ == '__main__':
    main()



