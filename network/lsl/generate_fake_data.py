from pylsl import StreamInfo, StreamOutlet, cf_float32
import time

def main():
    info = StreamInfo('RValues', 'Markers', 3, 0, cf_float32, 'asdfqwer1234')
    outlet = StreamOutlet(info)
    sample = [0.0, 0.0, 0.0]

    while 1:
        outlet.push_sample(sample)
        print("Sample: ", sample)
        sample[0] += .01
        if sample[0] >= 1.0:
            sample[0] -= 1.0
        sample[1] += .02
        if sample[1] >= 1.0:
            sample[1] -= 1.0
        sample[2] += .03
        if sample[2] >= 1.0:
            sample[2] -= 1.0
        time.sleep(.5)

if __name__== '__main__':
    main()