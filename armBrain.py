import numpy as np  # Module that simplifies computations on matrices
import matplotlib.pyplot as plt  # Module used for plotting
from pylsl import StreamInlet, resolve_byprop  # Module to receive EEG data
import threading
import multiprocessing
import utils  # Our own utility functions
from time import sleep
import requests
import os
import serial
from Naked.toolshed.shell import execute_js, muterun_js
#ser = serial.Serial('/dev/ttyACM0', 9600)

def runJ(name):
    success = execute_js('brainRep.js')
    if success:
        print(success)
    else:
        print("Error")

delta_waves = 0
theta_waves = 0
alpha_waves = 0
beta_waves = 0

prev = 0

class Band:
    Delta = 0
    Theta = 1
    Alpha = 2
    Beta = 3


BUFFER_LENGTH = 5

EPOCH_LENGTH = 1

OVERLAP_LENGTH = 0.8

SHIFT_LENGTH = EPOCH_LENGTH - OVERLAP_LENGTH

INDEX_CHANNEL = [0]
#Set global variables


print('Looking for an EEG stream...')
streams = resolve_byprop('type', 'EEG', timeout=2)
#Look for eeg streams spawned from running museTest.py
if len(streams) == 0:
    #If no streams are found
    raise RuntimeError('Can\'t find EEG stream.')
    #Exception and message to user

print("Start acquiring data")
inlet = StreamInlet(streams[0], max_chunklen=12)
#Create an inlet to read data from first stream found
eeg_time_correction = inlet.time_correction()

info = inlet.info()
description = info.desc()
#Get info on stream inlet
fs = int(info.nominal_srate())


eeg_buffer = np.zeros((int(fs * BUFFER_LENGTH), 1))
print(eeg_buffer)
filter_state = None  # for use with the notch filter

n_win_test = int(np.floor((BUFFER_LENGTH - EPOCH_LENGTH) /
                          SHIFT_LENGTH + 1))
band_buffer = np.zeros((n_win_test, 4))

def send(numb):
     ser.write(str(numb).encode())
     print(ser.readline().decode())

bigList = []

counts = 0

alr1 = 0
alr2 = 0
alr3 = 0

prevAlph = 0
prevThet = 0
prevDel = 0
prevBet = 0

prevList = [0, 0, 0, 0]

file1 = "mainDir.txt"

numbs = 0

if __name__ == '__main__':
    try:
        while True:
            eeg_data, timestamp = inlet.pull_chunk(
                timeout=1, max_samples=int(SHIFT_LENGTH * fs))
            #Pull sample data from the stream inlet

            ch_data = np.array(eeg_data)[:, INDEX_CHANNEL]
            #Create a numpy array of the data obtained

            eeg_buffer, filter_state = utils.update_buffer(
                eeg_buffer, ch_data, notch=True,
                filter_state=filter_state)
            #Update eeg buffer with data pulled from inlet

            data_epoch = utils.get_last_data(eeg_buffer,
                                             EPOCH_LENGTH * fs)
            #Pull1 new row from the buffer array

            band_powers = utils.compute_band_powers(data_epoch, fs)
            #Break down eeg buffer into different frequency bands to distinguish between each individual signal measured
            #Every signal we want to measure(alpha, beta, theta, delta) has a specific frequency range with strict limits to each. By applying these limits, we can extract the specific values we want
            band_buffer, _ = utils.update_buffer(band_buffer,
                                                 np.asarray([band_powers]))
            #Update eeg buffer with new frequency bands

            #smooth_band_powers = np.mean(band_buffer, axis=0)

            delta_waves = band_powers[Band.Delta]
            theta_waves = band_powers[Band.Theta]
            alpha_waves = band_powers[Band.Alpha]
            beta_waves = band_powers[Band.Beta]
            #Extract wave amplitude for each band power measured
            lists = [alpha_waves, theta_waves, delta_waves, beta_waves]
            spikeList = []
            """print(alpha_waves)
            print(theta_waves)
            print(delta_waves)
            print(beta_waves)"""
            if alpha_waves > (prevAlph + 0.47):
                spikeList.append('Alpha')
            if theta_waves > (prevThet + 0.47):
                spikeList.append('Theta')
            if delta_waves > (prevDel + 0.47):
                spikeList.append('Delta')
            if beta_waves > (prevBet + 0.47):
                spikeList.append('Beta')
            #Quick blink = alpha + theta, Jaw clench = beta, entire face = all 4, slow eyebrow raise = theta + delta, eyebrow raise + jaw clench = theta + delta + beta
            print(spikeList)
            if len(spikeList) == 2:
                if 'Delta' in spikeList and 'Theta' in spikeList:
                    print("Send")
                    print(numbs)
                    reqStr = 'http://eduvh.herokuapp.com/' + str(numbs) + '/posM'
                    r =requests.get(reqStr)
                    print(r)
                    numbs = 0
                if 'Delta' in spikeList and 'Beta' in spikeList:
                    print("Enter")
                    numbs += 1
                    print(numbs)

            if len(spikeList) == 1:
                if 'Beta' in spikeList:
                    print("Enter")
                    numbs += 1
                    print(numbs)
                    #print(r)

            if len(spikeList) == 3:
                if 'Delta' in spikeList and 'Theta' in spikeList and 'Alpha' in spikeList:
                    print("Send")
                    print(numbs)
                    reqStr = 'http://eduvh.herokuapp.com/' + str(numbs) + '/posM'
                    r =requests.get(reqStr)
                    print(r)
                    numbs = 0
                if 'Beta' in spikeList and 'Theta' in spikeList and 'Alpha' in spikeList:
                    print("Send")
                    print(numbs)
                    reqStr = 'http://eduvh.herokuapp.com/' + str(numbs) + '/posM'
                    r =requests.get(reqStr)
                    print(r)
                    numbs = 0
            if len(spikeList) == 4:
                print("Send")
                print(numbs)
                reqStr = 'http://eduvh.herokuapp.com/' + str(numbs) + '/posM'
                r =requests.get(reqStr)
                print(r)
                numbs = 0
            prevAlph = alpha_waves
            prevBet = beta_waves
            prevDel = delta_waves
            prevThet = theta_waves

    except KeyboardInterrupt:
        #If user exits
        print("   ")
        print("   ")
        print("Deads")
        print("   ")
        print("   ")
        print('Closing!')
        r =requests.get('http://eduvh.herokuapp.com/0/posM')
        print(r)
