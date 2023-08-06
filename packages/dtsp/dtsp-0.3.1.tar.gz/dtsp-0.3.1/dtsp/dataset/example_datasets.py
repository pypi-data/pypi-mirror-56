# encoding: utf-8
"""
@author : zhirui zhou
@contact: evilpsycho42@gmail.com
@time   : 2019/11/19 16:02
"""
from .curve import arima
from .dataset import SimpleSeq2SeqDataSet, SimpleWaveNetDataSet, Seq2SeqDataSet
from .utils import walk_forward_split
import numpy as np
from torch.utils.data import Subset
import pandas as pd
from pathlib import Path


def example_simple_seq2seq_arima(seqs_lens, enc_lens, dec_lens, n_test):
    ar = {1: 0.51, 3: 0.39, 12: 0.1}
    ma = {1: 0.62, 2: 0.20, 6: 0.18}
    var = 1.

    series = arima(seqs_lens, ar=ar, ma=ma, var=var)
    mu = series[:-(n_test + dec_lens)].mean()
    std = series[:-(n_test + dec_lens)].std()
    series = (series - mu) / std

    dset = SimpleSeq2SeqDataSet(series, enc_lens, dec_lens)
    idxes = np.arange(len(dset))
    train_idx, valid_idx = walk_forward_split(idxes, enc_lens, dec_lens, n_test)
    train = Subset(dset, train_idx)
    valid = Subset(dset, valid_idx)
    return train, valid


def example_simple_wavenet_arima(seqs_lens, enc_lens, dec_lens, n_test):
    ar = {1: 0.51, 3: 0.39, 12: 0.1}
    ma = {1: 0.62, 2: 0.20, 6: 0.18}
    var = 1.

    series = arima(seqs_lens, ar=ar, ma=ma, var=var)
    mu = series[:-(n_test + dec_lens)].mean()
    std = series[:n_test + dec_lens].std()
    series = (series - mu) / std

    dset = SimpleWaveNetDataSet(series, enc_lens, dec_lens)
    idxes = np.arange(len(dset))
    train_idx, valid_idx = walk_forward_split(idxes, enc_lens, dec_lens, n_test)
    train = Subset(dset, train_idx)
    valid = Subset(dset, valid_idx)
    return train, valid


def example_data():
    data_path = Path(__file__).resolve().parent / "data.csv"
    data = pd.read_csv(str(data_path), parse_dates=['date_time'], index_col="date_time")
    series = data.values
    month = data.index.month.values
    return {'series': series, 'categorical_var': month}


def example_1(enc_lens, dec_lens, n_test, model_type='seq2seq'):
    data_path = Path(__file__).resolve().parent / "data.csv"
    data = pd.read_csv(str(data_path), parse_dates=['date_time'], index_col="date_time")

    series = data.values
    mu = series[:-(n_test + dec_lens - 1)].mean(axis=0)
    std = series[:-(n_test + dec_lens - 1)].std(axis=0)
    series = (series - mu) / std
    categorical_var = data.index.month.values
    if model_type == 'seq2seq':
        dset = Seq2SeqDataSet(series, enc_lens, dec_lens, categorical_var=categorical_var)
        idxes = np.arange(len(dset))
        train_idx, valid_idx = walk_forward_split(idxes, enc_lens, dec_lens, n_test)
        train = Subset(dset, train_idx)
        valid = Subset(dset, valid_idx)
        return train, valid
    elif model_type == 'simple_seq2seq':
        dset = Seq2SeqDataSet(series, enc_lens, dec_lens)
        idxes = np.arange(len(dset))
        train_idx, valid_idx = walk_forward_split(idxes, enc_lens, dec_lens, n_test)
        train = Subset(dset, train_idx)
        valid = Subset(dset, valid_idx)
        return train, valid
    elif model_type == 'simple_wavenet':
        dset = SimpleWaveNetDataSet(series, enc_lens, dec_lens)
        idxes = np.arange(len(dset))
        train_idx, valid_idx = walk_forward_split(idxes, enc_lens, dec_lens, n_test)
        train = Subset(dset, train_idx)
        valid = Subset(dset, valid_idx)
        return train, valid
