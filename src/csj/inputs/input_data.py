#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Make input data (CSJ corpus)."""

import os
import pickle
import numpy as np
from tqdm import tqdm

from utils.util import mkdir
from utils.inputs.segmentation import segment_htk


def read_htk(htk_paths, speaker_dict, global_norm, is_training,
             save_path=None, train_mean=None, train_std=None):
    """Read HTK files.
    Args:
        htk_paths: list of paths to HTK files
        speaker_dict: dictionary of speakers
            key => speaker name
            value => dictionary of utterance information of each speaker
                key => utterance index
                value => [start_frame, end_frame, transcript]
        global_norm: if True, normalize input data by global mean & std of train data
                     if False, normalize data by mean & std per speaker
        is_training: training or not
        save_path: path to save npy files
        train_mean: global mean over train data
        train_std: global standard deviation over train data
    Returns:
        train_mean: global mean over train data
        train_std: global standard deviation over train data
    """
    # read each HTK file
    print('===> Reading HTK files...')
    return_list = []
    for htk_path in tqdm(htk_paths):
        speaker_name = os.path.basename(htk_path).split('.')[0]
        return_list.append(
            segment_htk(htk_path, speaker_name, speaker_dict[speaker_name],
                        speaker_norm=not global_norm, sil_duration=50))

    input_data_dict_list, train_mean_list, train_std_list,  total_frame_num_list = [], [], [], []
    for return_element in return_list:
        input_data_dict_list.append(return_element[0])
        train_mean_list.append(return_element[1])
        train_std_list.append(return_element[2])
        total_frame_num_list.append(return_element[3])

    if is_training:
        feature_dim = train_mean_list[0].shape[0]
        # compute global mean
        print('===> Computing global mean over train data...')
        train_global_mean = np.empty((feature_dim,), dtype=np.float64)
        total_frame_num = np.sum(total_frame_num_list)
        for i, input_data_dict in enumerate(tqdm(input_data_dict_list)):
            total_frame_num_speaker = total_frame_num_list[i]
            train_global_mean += train_mean_list[i]
        train_global_mean = train_global_mean / float(total_frame_num)

        # compute global standard deviation
        print('===> Computing global std over train data...')
        train_global_std = np.empty((feature_dim,), dtype=np.float64)
        for i, input_data_dict in enumerate(tqdm(input_data_dict_list)):
            # compute square values between features & global mean per speaker
            frame_offset = 0
            total_frame_num_speaker = total_frame_num_list[i]
            train_data_speaker = np.empty(
                (total_frame_num_speaker, feature_dim))
            for input_data_utt in input_data_dict.values():
                frame_num_utt = input_data_utt.shape[0]
                train_data_speaker[frame_offset:frame_offset +
                                   frame_num_utt] = input_data_utt
                frame_offset += frame_num_utt
            train_global_std += sqrt_sum(train_data_speaker, train_global_mean)
        train_global_std = np.power(
            train_global_std / float(total_frame_num), 0.5)

        if save_path is not None:
            # save global mean & std
            statistics_save_path = '/'.join(save_path.split('/')[:-1])
            np.save(os.path.join(statistics_save_path,
                                 'train_mean.npy'), train_global_mean)
            np.save(os.path.join(statistics_save_path,
                                 'train_std.npy'), train_global_std)

    if save_path is not None:
        # save input data
        print('===> Saving input data...')
        frame_num_dict = {}
        for input_data_dict in tqdm(input_data_dict_list):
            for key, input_data_utt in input_data_dict.items():
                # normalize by global mean & std over train data
                if global_norm:
                    input_data_utt = (
                        input_data_utt - train_global_mean) / train_global_std

                speaker_name, utt_index = key.split('_')
                mkdir(os.path.join(save_path, speaker_name))
                input_data_save_path = os.path.join(
                    save_path, speaker_name, key + '.npy')

                np.save(input_data_save_path, input_data_utt)
                frame_num_dict[key] = input_data_utt.shape[0]

        # save the frame number dictionary
        frame_num_dict_save_path = '/'.join(save_path.split('/')[:-1])
        print('===> Saving : frame_num.pickle')
        with open(os.path.join(frame_num_dict_save_path, 'frame_num.pickle'), 'wb') as f:
            pickle.dump(frame_num_dict, f)

    return train_mean, train_std


def sqrt_sum(inputs, global_mean):
    feature_dim = inputs[0].shape[0]
    value_sqrt_sum = np.zeros((feature_dim,))
    for input_vec in inputs:
        value_sqrt_sum += np.power((input_vec -
                                    global_mean), 2, dtype=np.float64)
    return value_sqrt_sum