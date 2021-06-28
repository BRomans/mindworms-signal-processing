from pylsl import StreamInfo, StreamOutlet, cf_float32
import time


class LSLDataSender:

    def __init__(self):
        unity_stream = StreamInfo('Unity', 'EEG', 2, 0, cf_float32, 'test')
        self.outlet = StreamOutlet(unity_stream)

    def send_sample(self, sample):
        self.outlet.push_sample(sample)
        time.sleep(.25)

