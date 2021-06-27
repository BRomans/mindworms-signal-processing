from pylsl import StreamInlet, resolve_stream
from threading import Thread


class LSLDataReceiver:

    def __init__(self):
        self.listen = False
        self.inlet = None
        self.thread = None
        self.sample = None

    def resolve_streams(self):
        print("looking for an EEG stream...")
        streams = resolve_stream('type', 'EEG')
        print("establishing stream inlet for")
        #print(streams[0].as_xml())
        # to establish a connection
        self.inlet = StreamInlet(streams[0])

    def start_listener(self):
        if self.inlet is None:
            print("no lsl inlet is established")
            return False
        if self.thread:
            print("already listening")
            return False
        self.thread = Thread(
            target=self._listen
        )
        self.listen = True
        self.thread.start()

    def stop_listener(self):
        self.listen = False
        self.thread.join()
        self.thread = None

    def run(self):
        self.resolve_streams()
        if self.inlet is None:
            print("no lsl inlet is established")
            return False
        self.listen = True
        self._listen()

    def _listen(self):
        while self.listen==True:
            self.sample, timestamp = self.inlet.pull_sample()

