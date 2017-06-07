#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Prepare for making dataset."""

import os
from os.path import join
import sys
from glob import glob

sys.path.append('../')
from utils.util import mkdir


class Prepare(object):
    """Prepare for making dataset."""

    def __init__(self):

        # path to timit data (set yourself)
        self.data_path = '/n/sd8/inaguma/corpus/timit/original/'
        self.train_data_path = join(self.data_path, 'train')
        self.test_data_path = join(self.data_path, 'test')

        # path to save directories (set yourself)
        self.dataset_path = mkdir('/n/sd8/inaguma/corpus/timit/dataset/')
        self.fbank_path = mkdir('/n/sd8/inaguma/corpus/timit/fbank/')

        # absolute path to this directory (set yourself)
        self.run_root_path = '/n/sd8/inaguma/src/asr/asr_preprocessing/src/timit/'

        self.__make()

    def __make(self):

        ####################
        # train
        ####################
        self.wav_train_paths = []
        self.text_train_paths = []
        self.word_train_paths = []
        self.phone_train_paths = []
        for file_path in glob(join(self.train_data_path, '*/*/*')):
            region_name, speaker_name, file_name = file_path.split('/')[-3:]
            ext = os.path.splitext(file_name)[1]
            if os.path.basename(file_name)[0: 2] in ['sx', 'si']:
                if ext == '.wav':
                    self.wav_train_paths.append(
                        join(self.train_data_path, file_path))
                elif ext == '.txt':
                    self.text_train_paths.append(
                        join(self.train_data_path, file_path))
                elif ext == '.wrd':
                    self.word_train_paths.append(
                        join(self.train_data_path, file_path))
                elif ext == '.phn':
                    self.phone_train_paths.append(
                        join(self.train_data_path, file_path))

        ####################
        # dev
        ####################
        # read speaker list
        speakers_dev = []
        with open(join(self.run_root_path, 'dev_speaker_list.txt'), 'r') as f:
            for line in f:
                line = line.strip()
                speakers_dev.append(line)

        self.wav_dev_paths = []
        self.text_dev_paths = []
        self.word_dev_paths = []
        self.phone_dev_paths = []
        for file_path in glob(join(self.test_data_path, '*/*/*')):
            region_name, speaker_name, file_name = file_path.split('/')[-3:]
            ext = os.path.splitext(file_name)[1]

            if speaker_name not in speakers_dev:
                continue
            elif os.path.basename(file_name)[0: 2] in ['sx', 'si']:
                if ext == '.wav':
                    self.wav_dev_paths.append(
                        join(self.test_data_path, file_path))
                elif ext == '.txt':
                    self.text_dev_paths.append(
                        join(self.test_data_path, file_path))
                elif ext == '.wrd':
                    self.word_dev_paths.append(
                        join(self.test_data_path, file_path))
                elif ext == '.phn':
                    self.phone_dev_paths.append(
                        join(self.test_data_path, file_path))

        ####################
        # test
        ####################
        # read speaker list
        speakers_test = []
        with open(join(self.run_root_path, 'test_speaker_list.txt'), 'r') as f:
            for line in f:
                line = line.strip()
                speakers_test.append(line)

        self.wav_test_paths = []
        self.text_test_paths = []
        self.word_test_paths = []
        self.phone_test_paths = []
        for file_path in glob(join(self.test_data_path, '*/*/*')):
            region_name, speaker_name, file_name = file_path.split('/')[-3:]
            ext = os.path.splitext(file_name)[1]

            if speaker_name not in speakers_test:
                continue
            elif os.path.basename(file_name)[0: 2] in ['sx', 'si']:
                if ext == '.wav':
                    self.wav_test_paths.append(
                        join(self.test_data_path, file_path))
                elif ext == '.txt':
                    self.text_test_paths.append(
                        join(self.test_data_path, file_path))
                elif ext == '.wrd':
                    self.word_test_paths.append(
                        join(self.test_data_path, file_path))
                elif ext == '.phn':
                    self.phone_test_paths.append(
                        join(self.test_data_path, file_path))

    def wav(self, data_type):
        """Get paths to wav files.
        Args:
            data_type: train or dev or test
        Returns:
            paths to wav files
        """
        if data_type == 'train':
            return sorted(self.wav_train_paths)
        elif data_type == 'dev':
            return sorted(self.wav_dev_paths)
        elif data_type == 'test':
            return sorted(self.wav_test_paths)

    def text(self, data_type):
        """Get paths to sentence-level transcription files.
        Args:
            data_type: train or dev or test
        Returns:
            paths to transcription files
        """
        if data_type == 'train':
            return sorted(self.text_train_paths)
        elif data_type == 'dev':
            return sorted(self.text_dev_paths)
        elif data_type == 'test':
            return sorted(self.text_test_paths)

    def word(self, data_type):
        """Get paths to word-level transcription files.
        Args:
            data_type: train or dev or test
        Returns:
            paths to transcription files
        """
        if data_type == 'train':
            return sorted(self.word_train_paths)
        elif data_type == 'dev':
            return sorted(self.word_dev_paths)
        elif data_type == 'test':
            return sorted(self.word_test_paths)

    def phone(self, data_type):
        """Get paths to phone-level transcription files.
        Args:
            data_type: train or dev or test
        Returns:
            paths to transcription files
        """
        if data_type == 'train':
            return sorted(self.phone_train_paths)
        elif data_type == 'dev':
            return sorted(self.phone_dev_paths)
        elif data_type == 'test':
            return sorted(self.phone_test_paths)


if __name__ == '__main__':
    prep = Prepare()

    print('===== train =====')
    print(len(prep.wav(data_type='train')))
    print(len(prep.text(data_type='train')))
    print(len(prep.word(data_type='train')))
    print(len(prep.phone(data_type='train')))

    print('===== dev ======')
    print(len(prep.wav(data_type='dev')))
    print(len(prep.text(data_type='dev')))
    print(len(prep.word(data_type='dev')))
    print(len(prep.phone(data_type='dev')))

    print('===== test =====')
    print(len(prep.wav(data_type='test')))
    print(len(prep.text(data_type='test')))
    print(len(prep.word(data_type='test')))
    print(len(prep.phone(data_type='test')))