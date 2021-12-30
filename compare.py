# coding: utf-8
__author__ = 'Roman Solovyev (ZFTurbo), IPPM RAS'

import os
import glob
import soundfile as sf
import numpy as np
import time
import argparse

INPUT_PATH = '../input/musdb18hq/test/'

"""
SDR - Source to distortion ratio   
SIR - Source to inferences ratio
SNR - Source to noise ration
SAR - Source to artifacts ratio
"""

def sdr(references, estimates):
    # compute SDR for one song
    delta = 1e-7  # avoid numerical errors
    num = np.sum(np.square(references), axis=(1, 2))
    den = np.sum(np.square(references - estimates), axis=(1, 2))
    num += delta
    den += delta
    return 10 * np.log10(num / den)


def parse_opt(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default='./input/test/', help='input directory with reference audio')
    parser.add_argument('--output', type=str, default='./output/', help='output directory with separated audio')
    if args:
        opt = parser.parse_args(args)
    else:
        opt = parser.parse_args()
    return opt


def main(opt):
    start_time = time.time()

    input_files = glob.glob(opt.input + '*/mixture.wav')
    print('Found files to process: {}'.format(len(input_files)))
    if len(input_files) == 0:
        print('Check input folder. Cant find any files!')
        exit()

    # Find which stems we want to process (using first folder in test)
    proc_type = glob.glob(os.path.dirname(input_files[0]) + '/*.wav')
    proc_type = [os.path.basename(f)[:-4] for f in proc_type]
    proc_type.remove('mixture')
    print('Calculate score for following stems: {}'.format(proc_type))

    scores = dict()
    for type in proc_type:
        scores[type] = []

    for f in input_files:
        folder_name = os.path.basename(os.path.dirname(f))
        print('Go folder: {}'.format(folder_name))

        for type in proc_type:
            in_path = os.path.join(opt.input, folder_name, type + '.wav')
            if not os.path.isfile(in_path):
                print('Warning: Cant find {}. Skip it!'.format(in_path))
                continue

            result_path = glob.glob(os.path.join(opt.output, folder_name) + '/*{}.wav'.format(type))
            if len(result_path) == 0:
                print('Warning: Cant find {}.wav in {}'.format(type, os.path.join(opt.output, folder_name)))
                continue
            if len(result_path) > 1:
                print('Warning: Found many files {}.wav in {}. Will use first one.'.format(type, os.path.join(opt.output, folder_name)))
            res_path = result_path[0]

            reference, sr1 = sf.read(in_path)
            estimate, sr2 = sf.read(res_path)
            references = np.expand_dims(reference, axis=0)
            estimates = np.expand_dims(estimate, axis=0)
            if estimates.shape != references.shape:
                print('Warning: Different length of WAV files: {} != {}. Skip it!'.format(estimates.shape, references.shape))
                continue

            song_score = sdr(references, estimates)[0]
            print('Type: {} SDR: {:.4f}'.format(type, song_score))
            scores[type].append(song_score)

    print('\nAveraged model results')
    for type in proc_type:
        if len(scores[type]) > 0:
            print('SDR {}: {:.4f}'.format(type, np.array(scores[type]).mean()))
        else:
            print('SDR {}: ---'.format(type))
    print('Proc time: {:.2f} sec'.format(time.time() - start_time))


if __name__ == '__main__':
    options = parse_opt()
    main(options)
