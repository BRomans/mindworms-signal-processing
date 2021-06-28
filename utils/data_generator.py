from utils.json_writer import JsonWriter
from pylsl import StreamInfo, StreamOutlet, cf_float32
import json
import time


class DataGenerator:

    def __init__(self, filename):
        info = StreamInfo('type', 'EEG', 32, 0, cf_float32, 'test')
        self.outlet = StreamOutlet(info)
        file = open(filename, )
        self.json_source = json.load(file)

    ''' Generate a stream of zero values except on channel 9 (SMR) and channel 23 (Beta) '''
    def generate_stream(self, delay=0):
        while True:
            for sample in self.json_source['stream']:
                f_sample = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,  0.0, 0.0, float(sample[0]), 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, float(sample[1]), 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # Convert string values to float
                self.outlet.push_sample(f_sample)
                print("Sending: ", f_sample)
                time.sleep(delay)


generator = DataGenerator('../data/20210628-103050_mindworms_recording.json')
generator.generate_stream()







