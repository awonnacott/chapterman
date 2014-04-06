import cPickle as pickle


def save(filename, db):
    file = open(filename, 'wb')
    pickle.dump(db, file)
    file.close()


def load(filename):
    file = open(filename, 'rb')
    db = pickle.load(file)
    file.close()
    return db


def same(filename, db): # VERY BAD
    return False