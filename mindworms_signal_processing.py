from network.lsl.lsl_data_receiver import LSLDataReceiver
import preprocessing.data_preprocessing as prep
import numpy as np
import time

from network.lsl.lsl_data_sender import LSLDataSender
from network.udp.udp_data_sender import UDPDataSender

CALIBRATION_TIMER = 30
SAMPLING_RATE = 512
SMR_CH = 9
BETA_CH = 22
MAX_SAMPLES = 500
CHANNEL = 0


class MindwormsSignalProcessing:

    def __init__(self, smr_ch=SMR_CH, beta_ch=BETA_CH):
        self.lsl_receiver = LSLDataReceiver()
        self.udp_sender = UDPDataSender()
        self.lsl_sender = LSLDataSender()
        self.buffer = []

        # SMR  channel 9 + Beta channel 22
        self.smr_ch = smr_ch
        self.beta_ch = beta_ch
        self.baseline_smr = []
        self.baseline_beta = []
        self.bs_smr = 0
        self.bs_beta = 0

    def calculate_baseline(self):
        t_end = time.time() + CALIBRATION_TIMER
        print("Calculating baseline values...")
        # calculating baseline
        while time.time() < t_end:
            sample = self.lsl_receiver.sample
            self.baseline_smr.append(sample[self.smr_ch])
            self.baseline_beta.append(sample[self.beta_ch])
        # calculating band power
        bs_smr_bp = prep.bandpower(self.baseline_smr, SAMPLING_RATE, [12, 15], relative=True)
        bs_beta_bp = prep.bandpower(self.baseline_beta, SAMPLING_RATE, [15, 18], relative=True)
        self.bs_smr = np.mean(bs_smr_bp)
        self.bs_beta = np.mean(bs_beta_bp)

        print("SMR baseline : ", self.bs_smr)
        print("Beta baseline : ", self.bs_beta)



    def start_processing(self):
        self.lsl_receiver.resolve_streams()
        self.lsl_receiver.start_listener()
        self.calculate_baseline()
        try:
            # get a new sample (you can also omit the timestamp part if you're not
            # interested in it)
            sample = self.lsl_receiver.sample
            # print(timestamp, sample)

            self.buffer.append(sample[self.smr_ch])
            self.buffer.append(sample[self.beta_ch])
            if len(self.buffer) > MAX_SAMPLES:
                self.buffer.pop(0)
                bp_smr = prep.bandpower(self.buffer, 512, [12, 15], window_sec=2, relative=True)
                bp_beta = prep.bandpower(self.buffer, 512, [15, 18], window_sec=2, relative=True)
                bp_smr_diff = float(bp_smr - self.bs_smr)
                bp_beta_diff = float(bp_beta - self.bs_beta)

                #file.write(bp_smr_diff, bp_beta_diff)
                bp_smr_diff = bp_smr_diff * 100000000
                bp_beta_diff = bp_beta_diff * 100000000
                print("SMR diff: ", bp_smr_diff)
                print("beta diff: ", bp_beta_diff)
                msg = "{:.10f}".format(bp_beta_diff) + " " + "{:.10f}".format(bp_smr_diff)
                sample = [bp_smr_diff, bp_beta_diff]
                self.udp_sender.send_message(msg)
                self.lsl_sender.send_sample(sample)
        except KeyboardInterrupt:
            print('\nClosing and saving data...')


if __name__ == '__main__':
    mw_signal_processing = MindwormsSignalProcessing()
    mw_signal_processing.start_processing()
