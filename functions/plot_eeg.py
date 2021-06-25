"""Example program to show how to read a multi-channel time series from LSL."""

from os import remove
from pylsl import StreamInlet, resolve_stream
import matplotlib.pyplot as plt


def main():
    # first resolve an EEG stream on the lab network
    print("looking for an EEG stream...")
    streams = resolve_stream('type', 'EEG')

    # create a new inlet to read from the stream
    inlet = StreamInlet(streams[0])


    sample_buffer = []
    
    max_samples = 40
    plot_interval = 10
    plotter_sample_counter = 0
    plt.ion()

    while True:
        # get a new sample (you can also omit the timestamp part if you're not
        # interested in it)
        sample, timestamp = inlet.pull_sample()
        plotter_sample_counter+=1

        for i in range(len(sample)):
            if len(sample_buffer) <= i:
                sample_buffer.append({"ts":[],"samples":[]})
            sample_buffer[i]["samples"].append(sample[i])
            sample_buffer[i]["ts"].append(timestamp)
            if len(sample_buffer[i]["ts"])>max_samples:
                sample_buffer[i]["ts"].pop(0)
                sample_buffer[i]["samples"].pop(0)
        
        if plotter_sample_counter == plot_interval:
            plotter_sample_counter = 0
            plt.gca().cla() # optionally clear axes
            for i in range(len(sample_buffer)):
                plt.plot(sample_buffer[i]["ts"], sample_buffer[i]["samples"], label='Channel '+str(i))
            plt.title("awesomeness")
            plt.legend(loc='upper left')
            plt.draw()
            plt.pause(0.0001)

if __name__ == '__main__':
    main()