from network.lsl.lsl_data_receiver import LSLDataReceiver
from preprocessing.data_preprocessing import bandpower
from network.lsl.lsl_data_sender import LSLDataSender
from network.udp.udp_data_sender import UDPDataSender
from utils.json_writer import JsonWriter
from threading import Thread
import numpy as np
import time

CALIBRATION_TIMER = 30
SAMPLING_RATE = 512
SMR_CH = 9
BETA_CH = 22
MAX_SAMPLES = 500
CHANNEL = 0
SCORE_MAGNIFIER = 1000


class MindwormsSignalProcessing:

    def __init__(self, smr_ch=SMR_CH, beta_ch=BETA_CH):
        self.lsl_receiver = LSLDataReceiver()
        self.lsl_receiver.resolve_streams()
        #self.lsl_receiver.start_listener()
        self.udp_sender = UDPDataSender()
        self.lsl_sender = LSLDataSender()
        self.json_writer = JsonWriter()
        self.buffer = []

        # SMR  channel 9 + Beta channel 22
        self.smr_ch = smr_ch
        self.beta_ch = beta_ch
        self.baseline_smr = []
        self.baseline_beta = []
        self.bs_smr = 0.0
        self.bs_beta = 0.0

    def countdown(self, timer):
        for i in range(timer):
            print(timer - i)
            #time.sleep(1)

    ''' Calculate baseline for using CALIBRATION_TIMER for the length'''
    def calculate_baseline(self):
        t_start = time.time()
        t_end = t_start + CALIBRATION_TIMER
        print("Calculating baseline values...")

        while time.time() < t_end:
            sample, timestamp = self.lsl_receiver.get_sample()  # this should be replaced with an asynchronous call
            self.baseline_smr.append(sample[self.smr_ch])
            self.baseline_beta.append(sample[self.beta_ch])

        # calculating band power
        bs_smr_bp = bandpower(self.baseline_smr, SAMPLING_RATE, [12, 15], relative=True)
        bs_beta_bp = bandpower(self.baseline_beta, SAMPLING_RATE, [15, 18], relative=True)
        self.bs_smr = np.mean(bs_smr_bp)
        self.bs_beta = np.mean(bs_beta_bp)

        print("SMR baseline power: ", self.bs_smr)
        print("Beta baseline power : ", self.bs_beta)

    def start_processing(self):
        self.calculate_baseline()
        try:
            while True:
                # get a new sample (you can also omit the timestamp part if you're not
                # interested in it)
                sample, timestamp = self.lsl_receiver.get_sample()  # this should be replaced with an asynchronous call
                self.buffer.append(sample[self.smr_ch])
                self.buffer.append(sample[self.beta_ch])
                if len(self.buffer) > MAX_SAMPLES:
                    self.buffer.pop(0)
                    bp_smr = bandpower(self.buffer, 512, [12, 15], window_sec=2, relative=True)
                    bp_beta = bandpower(self.buffer, 512, [15, 18], window_sec=2, relative=True)
                    bp_smr_diff = float(bp_smr - self.bs_smr)
                    bp_beta_diff = float(bp_beta - self.bs_beta)
                    self.json_writer.add_sample(sample[self.smr_ch], sample[self.beta_ch])
                    bp_smr_diff = bp_smr_diff * SCORE_MAGNIFIER
                    bp_beta_diff = bp_beta_diff * SCORE_MAGNIFIER
                    msg = "{:.10f}".format(bp_beta_diff) + " " + "{:.10f}".format(bp_smr_diff)
                    sample = [bp_smr_diff, bp_beta_diff]
                    print('Sending:', sample)
                    self.udp_sender.send_message(msg)
                    self.lsl_sender.send_sample(sample)
        except KeyboardInterrupt:
            #self.lsl_receiver.stop_listener()
            self.json_writer.write_file('data')
            print('\nClosing and saving data...')


if __name__ == '__main__':
    mw_signal_processing = MindwormsSignalProcessing()
    time.sleep(1)
    mw_signal_processing.start_processing()
