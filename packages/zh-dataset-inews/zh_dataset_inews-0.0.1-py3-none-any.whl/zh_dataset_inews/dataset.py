
import pickle


class Item:

    def __init__(self, path):
        self.path = path

    def __get__(self, obj, objtype=None):
        with open(self.path, 'rb') as fp:
            titles, contents, labels = pickle.load(fp)
        return titles, contents, labels


class Dataset:
    train = Item('./train.pkl')
    test = Item('./test.pkl')
    dev = Item('./dev.pkl')


dataset = Dataset()
