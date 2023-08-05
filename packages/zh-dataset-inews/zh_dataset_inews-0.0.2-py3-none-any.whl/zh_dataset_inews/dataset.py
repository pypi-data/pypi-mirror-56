# -*- coding: utf-8 -*-
import os
import pickle

CURRENT_DIR = os.path.realpath(
    os.path.dirname(__file__)
    if '__file__' in dir() else
    os.path.dirname('.'))


class Item:

    def __init__(self, path):
        self.path = path

    def __get__(self, obj, objtype=None):
        with open(self.path, 'rb') as fp:
            titles, contents, labels = pickle.load(fp)
        return titles, contents, labels


class Dataset:
    train = Item(os.path.join(CURRENT_DIR, 'train.pkl'))
    test = Item(os.path.join(CURRENT_DIR, 'test.pkl'))
    dev = Item(os.path.join(CURRENT_DIR, 'dev.pkl'))


dataset = Dataset()
