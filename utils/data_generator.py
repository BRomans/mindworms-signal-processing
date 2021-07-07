from pylsl import StreamInfo, StreamOutlet, cf_float32
import numpy as np
import json
import time


class DataGenerator:

    def __init__(self, filename, n_channels=32):
        info = StreamInfo('type', 'EEG', n_channels, 0, cf_float32, 'test')
        self.n_channels = n_channels
        self.outlet = StreamOutlet(info)
        file = open(filename, )
        self.json_source = json.load(file)

    ''' Generate a stream of zero values except on channel 9 (SMR) and channel 23 (Beta) '''
    def generate_stream(self, delay=0.0, idx_smr=9, idx_beta=22):
        while True:
            for sample in self.json_source['stream']:
                f_sample = np.zeros(self.n_channels)  # Convert string values to float
                f_sample[idx_smr] = float(sample[0])
                f_sample[idx_beta] = float(sample[1])
                self.outlet.push_sample(f_sample.tolist())
                print("Sending: ", list(f_sample))
                time.sleep(delay)


generator = DataGenerator('../data/20210628-103050_mindworms_recording.json', 34)
generator.generate_stream(0.25, 9, 32)







