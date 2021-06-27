from network.lsl.lsl_data_receiver import LSLDataReceiver
import preprocessing.data_preprocessing as prep
import numpy as np
import time

CALIBRATION_TIMER = 30


class MindwormsSignalProcessing:

    def __init__(self, max_samples=500, channel=0, smr_ch=9, beta_ch=22):
        self.lsl_receiver = LSLDataReceiver()
        self.buffer = []
        self.max_samples = max_samples
        self.channel = channel

        # SMR  channel 9 + Beta channel 22
        self.smr_ch = smr_ch
        self.beta_ch = beta_ch
        self.baseline_smr = []
        self.baseline_beta = []
        self.bs_smr = 0
        self.bs_beta = 0

    def calculate_baseline(self):
        t_end = time.time() + CALIBRATION_TIMER
        print("Calculating baseline values")
        # calculating baseline
        while time.time() < t_end:
            sample = self.lsl_receiver.sample
            self.baseline_smr.append(sample[self.smr_ch])
            self.baseline_beta.append(sample[self.beta_ch])
        # calculating band power
        bs_smr_bp = prep.bandpower(self.baseline_smr, 512, [12, 15], relative=True)
        bs_beta_bp = prep.bandpower(self.baseline_beta, 512, [15, 18], relative=True)
        self.bs_smr = np.mean(bs_smr_bp)
        self.bs_beta = np.mean(bs_beta_bp)

        print("SMR baseline : ", self.bs_smr)
        print("Beta baseline : ", self.bs_beta)



    def start_processing(self):
        self.lsl_receiver.resolve_streams()
        self.lsl_receiver.start_listener()
        try:
            print("hello")
        except KeyboardInterrupt:
            print('\nClosing and saving data...')


if __name__ == '__main__':
    mw_signal_processing = MindwormsSignalProcessing()
    mw_signal_processing.start_processing()
