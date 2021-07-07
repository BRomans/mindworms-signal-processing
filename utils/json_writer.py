import json
from datetime import datetime

FOLDER = '../data'


class JsonWriter:

    def __init__(self, user='test'):
        self.data = {'stream': [], 'smr': [], 'beta': []}
        self.filename = user + '_' + str(datetime.now().strftime("%Y%m%d-%H%M%S")) + '_mindworms_recording'

    ''' Add sample to the dictionary'''
    def add_sample(self, smr, beta):
        self.data['stream'].append([smr, beta])
        self.data['smr'].append(smr)
        self.data['beta'].append(beta)

    ''' Write the dictionary to file'''
    def write_file(self, folder=FOLDER):
        with open(folder + '/' + self.filename + '.json', 'w+') as f:
            json.dump(self.data, f, indent=4)

    ''' Convert old .txt format into json'''
    def convert_textfile(self, file):
        with open(file + '.txt', 'r') as file:
            for line in file:
                if line.strip():
                    smr, beta = line.split()
                    self.add_sample(smr, beta)
                    print(smr, beta)
            self.write_file()

    ''' Convert old .txt format into json'''

    def convert_textfile_single_line(self, file):
        with open(file + '.txt', 'r') as file:
            for line in file:
                for word in line.split():
                    counter = 0
                    if word.strip():
                        smr = ''
                        beta = ''
                        if counter == 0:
                            smr = word
                            counter += 1
                        if counter == 1:
                            beta = word
                            counter -= 1
                        self.add_sample(smr, beta)
                        print(str(smr), str(beta))
            self.write_file()


